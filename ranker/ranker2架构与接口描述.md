# Matrix Ranker2 架构与接口描述

##一 基本介绍
Matrix Ranker是对人脸,车辆,非机动车,人体等目标的特征(Feature)进行分数计算([0.0-1.0])并比对排序的服务. Ranker2基于原Ranker1和ImageSearch两个项目,重新设计和开发, 实现了单机十亿级别的特征比对能力.同时对多种目标的特征比对进行抽象和归纳, 在内部实现了多种特征存储,搜索和计算的统一.

Ranker2使用磁盘+内存+显存作数据存储,使用CPU+GPU作比对计算. 服务接口使用GRPC+Protobuf定义,并提供同构的Restful接口. 

为了便于描述, 以下介绍中主要使用GRPC+Protobuf来描述

### 1. 对比服务类型
Ranker比对计算主要分为三种类型:

    - 1:1 输入为两个特征f1和f2, 服务输出两个特征计算后的分数.
    - 1:n 输入为特征f和候选特征列表{f1,f2, f3, ..., fn}, 服务计算f和候选n个特征的分数并排序返回.
    - 1:N 输入为特征f和比对库ID, 服务分别计算f和对比库中符合条件的特征的分数,并排序返回top k个结果. k的值由调用者制定.
    
### 2. 特征属性
为了有效的存储,搜索和计算特征,Ranker2中的特征都必须具备以下四个属性. 这个四个属性也是在比对搜索过程中主要使用的属性,具有最高的性能.

1. 特征Id(Id, string类型) 该属性唯一代表了一个特征. 对于同一个Ranker2示例,不允许存在相同的Id.
2. 库Id (RepoId, int32类型) 该属性表明一个特征所属于的特征库. 理论上具有同一个RepoId的特征会被连续地存储在同一个地方(磁盘/内存/显存), 因此具有更高效地存储和读取性能. 对于用户而言,可以灵活地使用RepoId来实现业务需求. 比如可以把黑名单,白名单和抓拍分别作为三个RepoID, 也可以把机动车,二轮车和行人作为三个RepoID.
3. 地点(Location, int32类型) 该属性表明一个特征的地点信息. 
4. 时间(Time, int64类型) 该属性表明一个特征的时间信息.

除了上面四个必需的属性外, 用户还可以添加自定义的属性. 自定义属性以Key-Value形式定义, Key的数据类型是string, value的数据类型是int32. 比如可以为每一个人脸特征定义"年龄"属性, 也可为车辆特征定义"车型"属性, 具体由用户根据业务需要来定义.
理论上, 每一个Ranker2示例最多可定义2^32个自定义属性, 这个最大值由多个库共享使用. 

### 3. 库级别(Repo Level)
为了进一步提升数据存储,搜索和计算的性能, 每一个库均定义了库级别. 库级别定义如下:

```protobuf
    // -库的级别
    enum RepoLevel {
        REPO_LEVEL_NOT_USED = 0;
        // -数据主要存储在磁盘上, 在计算过程中会发生磁盘-内存间交换. 支持十亿级别的数据.
        REPO_LEVEL_ON_STORAGE = 1;
        // -未实现. 数组存储在内存上
        REPO_LEVEL_ON_RAM = 2;
        // -数据存储在GPU显存上, 在计算过程中直接使用, 不需要发生IO操作
        REPO_LEVEL_ON_GPU = 3;
        // -未实现. 数据部分在内存, 部分在磁盘
        REPO_LEVEL_ON_RAM_STORAGE = 4;
        // -未实现. 数据部分在显存, 部分在磁盘
        REPO_LEVEL_ON_GPU_STORAGE = 5;
        // -未实现. 数据部分在内存, 部分在显存
        REPO_LEVEL_ON_RAM_GPU = 6;
        // -未实现. 数据部分在内存, 部分在显存, 部分在磁盘
        REPO_LEVEL_ON_RAM_GPU_STORAGE = 7;
    }
```
  
目前Ranker2中仅支持REPO_LEVEL_ON_STORAGE = 1和REPO_LEVEL_ON_GPU = 3两种模式,其他模式会在之后的版本中陆续支持.

- REPO_LEVEL_ON_STORAGE = 1 表示数据存储在磁盘上, 在计算过程中会从磁盘中读取数据(带有部分缓存优化). 这种模式适用与大数据量(10亿级别)的库, 由于数据量巨大, 比对计算的延迟为1-10秒级别.
- REPO_LEVEL_ON_GPU = 3 表示数据存储在GPU显存上, 在系统启动过程中会一次性加载到显存中. 该模式适合比较小规模的数据量(与显存大小有关), 但是计算速度非常快(小于1秒).

### 4. 库/特征操作

对库和特征的操作是典型的CRUD类操作,即可以对库和特征进行增删改查类操作. 在增加类操作时需要指定唯一ID和必要的信息.其他操作使用唯一ID作为标示进行.
如果在查询库时不指定ID,则返回所有的库列表.
```protobuf

    // -库操作类型, 分为增加, 删除, 更新和查找
    enum RepoOperation {
        // -默认操作, 不可用
        REPO_OPERATION_DEFAULT = 0;
        // -增加一个新的库, 调用者需要保证库ID唯一
        REPO_OPERATION_ADD = 1;
        // -删除一个已存在的库
        REPO_OPERATION_DELETE = 2;
        // -更新一个已存在的库
        REPO_OPERATION_UPDATE = 3;
        // -查找一个或多个已存在的库
        REPO_OPERATION_QUERY = 4;
    }
    
    // -特征操作类型, 分为增加, 删除, 更新和查找
    enum ObjectOperation {
        // -默认操作, 不可用
        OBJECT_OPERATION_DEFAULT = 0;
        // 增加一个新特征, 调用者需要保证特征ID唯一
        OBJECT_OPERATION_ADD = 1;
        // 删除一个已存在的特征
        OBJECT_OPERATION_DELETE = 2;
        // 更新一个已存在的特征
        OBJECT_OPERATION_UPDATE = 3;
        // 查询一个或多个已存在的特征
        OBJECT_OPERATION_QUERY = 4;
    }

```

### 5. 错误码定义
```
    STORAGE_ERR_OK = 0,
    STORAGE_ERR_SYSTEM_ERROR = 401,

    STORAGE_ERR_FEATURE_LEN_INVALID = 408,
    STORAGE_ERR_FEATURE_EXISTS = 409,
    STORAGE_ERR_FEATURE_NOT_EXISTS = 410,
    STORAGE_ERR_FEATURE_DATA_INVALID =411,

    STORAGE_ERR_REPO_EXISTS = 420,
    STORAGE_ERR_REPO_NOT_EXISTS = 421,
    STORAGE_ERR_REPO_PARAM_INVALID = 422,

    STORAGE_ERR_RANK_PARAM_TIME_INVALID =450,
    STORAGE_ERR_RANK_PARAM_LOC_INVALID =451,
    STORAGE_ERR_RANK_PARAM_REPO_INVALID =452,
    STORAGE_ERR_RANK_PARAM_OTHERS_INVALID =459

```

## 二 服务接口定义
Ranker2服务的主要接口为库操作,特征操作和特征比对三个接口. 为了与之前的版本兼容, 原有的接口依然保留, 但是不建议继续使用, 由于缺少必要的测试,可能带来不可预料的结果.

库操作和特征操作是典型的CRUD类操作,及对数据的增删改查操作. 由于特征比对本身比较特殊, 因此定义一个单独的接口. 这三个接口的GRPC定义如下.并在后续章节作详细说明.

```protobuf
    // -特征库操作服务接口,实现库的CRUD操作
    rpc RepoOperation (RankRepoOpRequest) returns (RankRepoOpResponse) {
    }
    // -特征操作服务接口, 实现特征的CRUD操作
    rpc ObjectFeatureOperation (RankFeatureOpRequest) returns (RankFeatureOpResponse) {
    }
    // -特征比对服务接口, 实现特征相似度的比对服务
    rpc RankFeature (RankFeatureRequest) returns (RankFeatureResponse) {
    }
```

### 1. 库(Repo)操作
库操作是对特征库的CRUD类操作. 在把特征添加到某个库之前, 必须显式地创建一个库并提供一系列的参数指明库的属性. 每个库均具有的属性包括库的ID, 库的级别, 库内特征的长度. 其他参数为可选项. 接口和主要的数据结构定义如下:
```protobuf

    // -特征库操作服务接口,实现库的CRUD操作
    rpc RepoOperation (RankRepoOpRequest) returns (RankRepoOpResponse) {
    }
    // -库操作服务请求
    message RankRepoOpRequest {
        // -请求上下文信息
        RankRequestContext Context = 1;
        // -库操作请求信息
        RankRepoOperation Repo = 2;
    }
    // -库操作服务返回
    message RankRepoOpResponse {
        // -返回上下文信息
        RankResponseContext Context = 1;
        // -库操作返回信息
        repeated RankRepoOperation Repos = 2;
    }
    // -库操作具体信息
    message RankRepoOperation {
        // -库ID, 必需. 增加库时需要保证唯一,否则返回错误. 其他操作需保证库ID存在, 否则返回错误
        int32 RepoId = 1;
        // -具体操作内容. 包括增加, 删除, 修改和查找
        RepoOperation Operation = 2;
        // -库级别. 在增加和修改时必需, 其他操作不需要. 修改库级别需要重新启动服务进程.
        RepoLevel Level = 3;//Level 1-CPU,3-GPU
        // -特征长度. 在增加库时必需且不可更新. 其他操作不需要.
        int32 FeatureLen = 4;
        // -特征的数据类型, 目前包括float和short两种. 在增加库时必须且不可更新. 其他操作不需要. 默认为float
        FeatureDataType FeatureDataType = 5;//0-float,1-short,2-int8
        // -库容量. 如果库级别定义为REPO_LEVEL_ON_GPU, 在增加库时必需, 表明库的最大容量. 其他级别和操作不需要.
        int32 Capacity = 6;
        // -库当前大小, 仅在查询时作为返回值使用
        int32 Size = 7;
        // -可选参数. 目前可用参数包括:
        // -DynamicLoadNumber, 合法的数字型. 在库级别定义为REPO_LEVEL_ON_GPU时有效. 表明在启动时,按照数据新旧,最多加载到显存中的特征条数
        // -GPUThreads, [1,1,0,1]字符串格式. 在库级别定义为REPO_LEVEL_ON_GPU时必需. 表明数据在多个GPU上的分布. [1,1,0,1]表示当前服务器有三个GPU卡, 但是数据被平均存储在0,1和3号GPU卡上.
        map<string, string> Params = 8;
    }
    // -库操作类型, 分为增加, 删除, 更新和查找
    enum RepoOperation {
        // -默认操作, 不可用
        REPO_OPERATION_DEFAULT = 0;
        // -增加一个新的库
        REPO_OPERATION_ADD = 1;
        // -删除一个已存在的库
        REPO_OPERATION_DELETE = 2;
        // -更新一个已存在的库
        REPO_OPERATION_UPDATE = 3;
        // -查找一个已存在的库
        REPO_OPERATION_QUERY = 4;
    }

```

注意!

1. 增加库时, 多数参数需要指定且跟库的级别有关系.
2. 查询库时, 如果不指定RepoId, 则返回所有的库列表. 如果制定RepoId且存在, 返回该库的详细信息, 否则报错
3. 删除库时, 必须指定RepoId且存在, 否则报错.
4. 更新库时, 必须指定RepoId且存在, 否则报错. 可更新的属性包括库的级别, 库容量, DynamicLoadNumber和GPUThreads属性, 且需要在重启进程后生效. 其他属性可不更改.

### 2. 特征(Feature)操作

特征操作包括对特征的增删改查. 增加特征时必须指定要存储的库ID, 特征本身的ID, 时间和地点信息. 服务接口和主要数据结构的定义如下:
```protobuf

    // -特征操作服务接口, 实现特征的CRUD操作
    rpc ObjectFeatureOperation (RankFeatureOpRequest) returns (RankFeatureOpResponse) {
    }
    // -特征操作请求
    message RankFeatureOpRequest {
        // -请求上下文
        RankRequestContext Context = 1;
        // -请求详细信息
        RankFeatureOperation Features = 2;
    }
    
    // -特征操作返回
    message RankFeatureOpResponse {
        // -返回上下文
        RankResponseContext Context = 1;
        // -返回详细信息
        RankFeatureOperation Features = 2;
    }
    // -特征操作请求信息
    message RankFeatureOperation {
        // -待操作特征所属于的库ID, 增加特征时必需.
        int32 RepoId = 1;
        // -操作类型, 增加, 删除, 更新或者查询
        ObjectOperation Operation = 2;
        // -特征列表. 可同时增加, 删除, 更新或者查询多条特征.
        repeated ObjectProperty ObjectFeatures = 3;
        // -可选参数. 暂时未使用
        map<string, string> Params = 4;
    }
    // -特征属性
    message ObjectProperty {
        // -特征ID, 唯一标示一个特征, 必需.
        string Id = 1;
        // -地点, 表示特征的地点信息. 在增加时必需. 更新时可选用于指定新值.
        int32 Location = 4;
        // -时间, 表示特征的时间信息. 在增加时必需. 更新时可选用于指定新值.
        int64 Time = 5;
        // -特征的BASE64表示. 在增加时必需. 更新时可选用于指定新值.
        string Feature = 7;
        // -特征的其他可选属性. Key为string类型, value为int32类型. Key如果不存在会自动创建. Key的总数量小于2^32
        map<string, int32> Attributes = 9;
    
        // 以下字段为保证兼容而保留,不再使用
        // Decrepcated
        int32 Type = 2;
        // Decrepcated
        ObjectOperation Operation = 3;
        // Decrepcated
        int32 Repository = 6;
        // Decrepcated
        map<string, string> Params = 8; // vehicle: Type, Color, Plates, is_front
    }
```

### 3. 特征(Feature)比对
特征比对接口接收一个特征值和一系列比对参数, 与目标特征进行相似度计算并根据分数排序返回Top K个结果. 目标特征可以通过接口指定,也可指定库ID,表示与库中存储的特征进行比对. 由于库内特征数量通常会很大,因此还需要传递一系列的比对参数, 用于指定过滤条件减少数据规模.
默认情况下, 需要传入库ID, 地点列表和时间范围, Ranker会根据这三个属性过滤出目标特征, 同时还可以指定自定义的属性,比如年龄或者车型等属性. 这些属性会在计算完成后再进行一次过滤,减少返回数据的数量.
此外, 还可以指定分页, 归一化等参数, 改变返回值的形式.
```protobuf
    // -特征比对服务接口, 实现特征相似度的比对服务
    rpc RankFeature (RankFeatureRequest) returns (RankFeatureResponse) {
    }
    
    // -特征比对服务请求
    message RankFeatureRequest {
        // -请求上下文
        RankRequestContext Context = 1;
        // -待比对的特征信息
        ObjectProperty ObjectFeature = 3;
        // -候选特征列表. 默认为空表示1:N比对, 不为空进行1:1或1:n比对
        repeated ObjectProperty ObjectCandidates = 4;
        // -比对参数列表, 可选值如下
        // -ConfidenceThreshold, 数据类型为float, 指定比对分数的最小阈值, 小于该值不返回, 默认为0表示不过滤
        // -MaxCandidates 数据类型为int, 指定返回Top K
        // -PageSize 数据类型为int, 分页返回值, 指定每页大小. 默认为0表示不分页
        // -PageIndex 数据类型为int, 分页页数
        // -RepoId 必需. 数据类型为int, 指定在哪个库中进行比对.
        // -Locations 必需. 数据类型为int, 并可使用逗号分割传入多个值. 比如"1,2,3"表示只在地点是1,2,3的特征中进行比对
        // -StartTime 必需. 数据类型为int64.
        // -EndTime 必需. 数据类型为int64, 与StartTime配合使用,指定被特征的时间范围.
        // -Normalization. 数据类型为bool, 指定是否需要对分数计算结果进行归一化处理. 默认为false
        // -ShowAttributes. 数据类型为bool, 指定是否返回比对结果的详细属性,比如时间,地点等信息. 默认为false
        // -FilterABC. 数据类型为int, 并可使用逗号分割传入多个值表示一个集合. 用于动态属性过滤, FliterABC表示过滤自定义的ABC属性, ABC属性值在传入的集合中
        // -RangeXYZ. 数据类型为int-int, 表示一个值的范围. 用于动态属性过滤, FliterXYZ表示过滤自定义的XYZ属性, 属性值在传入的范围之间.
        map<string, string> Params = 6;
    
        // deprecated. 旧参数, 不再使用
        int32 MaxCandidates = 5; // 比对输出条目限制（0为不限制）
        // deprecated, 旧参数, 不再使用
        FeatureVector Feature = 2; // not used
    }
    
    // -特征比对服务返回
    message RankFeatureResponse {
        // -返回上下文
        RankResponseContext Context = 1;
        // -比对结果列表
        repeated RankItem Candidates = 2;
    }
    
    // -比对结果项
    message RankItem {
        // -特征Id
        string Id = 1;
        // -比对分数, [0.0-1.0]之间, 1.0表示相似度最接近
        float Score = 2;
        // -特征所在库Id, 默认不返回
        int32 RepoId = 7;
        // -特征地点信息, 默认不返回
        int32 Location = 8;
        // -特征时间信息, 默认不返回
        int64 Time = 9;
        // -特征其他属性, 默认不返回
        map<string, int32> Attributes = 6;
    
        // deprecated. 旧版本, 不再使用
        string Name = 3;
        // deprecated. 旧版本, 不再使用
        string URI = 4;
        // deprecated. 旧版本, 不再使用
        string Data = 5;
    }
```


