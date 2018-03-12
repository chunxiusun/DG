/**
 * The first thing to know about are types. The available types in Thrift are:
 *
 *  bool        Boolean, one byte
 *  byte        Signed byte
 *  i16         Signed 16-bit integer
 *  i32         Signed 32-bit integer
 *  i64         Signed 64-bit integer
 *  double      64-bit floating point value
 *  string      String
 *  binary      Blob (byte array)
 *  map<t1,t2>  Map from one type to another
 *  list<t1>    Ordered list of one type
 *  set<t1>     Set of unique elements of one type
 *
 * Did you also notice that Thrift supports C style comments?
 */


namespace cpp LibraFService

// port of thrift
const i32 DEFAULT_PORT = 9090

// error type
enum RpcLibraFErrorType {
	RPC_UNDEFINED_ERROR = 0x0fffffff,	//　未知错误
	
	RPC_SENSOR_CONNECT_ERROR = 0x10000001,	// 相机连接错误
	RPC_SENSOR_NUMBER_ERROR = 0x10000002,	// 相机个数有误
	RPC_SENSOR_NOT_USB3_ERROR = 0x10000003,	// 相机USB接口不是USB3.0
	RPC_SENSOR_START_ERROR = 0x10000004,	// 相机启动报错
	RPC_SENSOR_GET_STATUS_ERROR = 0x10000005,	// 无法获取相机状态
	RPC_SENSOR_SET_STATUS_ERROR = 0x10000006,	//　无法设置相机状态
	RPC_SENSOR_GET_IMG_DATA_ERROR = 0x10000007,	// 无法获取相机图像
	RPC_SENSOR_READ_NONSTART_CAMERA_ERROR = 0x10000008,	//　
	RPC_SENSOR_GET_IMG_DATA_TIMEOUT_ERROR = 0x10000009,	// 获取相机图像超时
	RPC_SENSOR_XU_ERROR = 0x1000000a,	// 相机xu通信出错，无法配置
	RPC_SENSOR_OCCLUSION_ERROR = 0x1000000b,	// 相机配置过快
	
	RPC_CALIBRATION_BUSY = 0x30000001,	//　正在校准，无法进行其他操作
	RPC_CATCHALL_BUSY = 0x30000002,	//　自动模式下，该操作无法实现
	RPC_UNDEFINED_BUSY = 0x30000003,	//　未知阻塞
	
	RPC_MOTOR_POWER_ERROR = 0x20000001,	// 点击电源或电机故障hard ware problem
	RPC_MOTOR_OCCLUSION_ERROR = 0x20000002,	// 手动操作电机过快或电机故障motor control signal get too fast
	RPC_MOTOR_ALGO_ERROR = 0x20000003,	// 电机控制算法报错
	RPC_MOTOR_INVALID_ANGLE = 0x20000004, // 目标位置超出电机转动范围限制
	
	RPC_INPUT_ERROR = 0x00000001,	//　输入数值越界，无法执行
	RPC_OPERATION_OCCLUSION_ERROR = 0x00000002,	// 操作过快　operation too fast
}

// 相机类型
enum RpcSensorType {
	RPC_WIDE = 0,	// 广角
	RPC_FOVEA = 1	// 长焦
}

// 电机工作模式
enum RpcMotorMode {
	RPC_TIME = 1,	// 在规定时间内转动到指定未知（暂时取消该模式 since. 20161115）
	RPC_SPEED = 2	//　电机以相应速度转动
}

// 人眼相机工作模式
enum RpcWorkMode{
	RPC_CORE_PASSIVE_WORKMODE = 0x01010000,	// 指哪打哪，munaully set the look at point
	RPC_CORE_CATCHALL_WORKMODE = 0x01020000,	// 自动检测，automatically look at all detected targets
	RPC_CORE_FOLLOW_WORKMODE = 0x01040000	//　自动跟踪(未实现)
}

// 云台控制电机移动方向
enum RpcRotateType{
	RpcMoveLeft,	
	RpcMoveRight,
	RpcMoveUp,
	RpcMoveDown,
	RpcMoveUpLeft,
	RpcMoveUpRight,
	RpcMoveDownLeft,
	RpcMoveDownRight
}

// 云台控制电机移动步长级别
enum RpcRotateStep{
	Rpc1Level,
	Rpc2Level,
	Rpc3Level,
	Rpc4Level,
	Rpc5Level,
	Rpc6Level,
}

// 抓拍类型
enum RpcSnapType{
	RpcFace = 0,
	RpcBody = 1,
	RpcCar = 2
}

//　码流类型
enum RpcStreamType{
	RpcMainStream,	// 主码流
	RpcSubStream	// 子码流
}

// OSD显示控制类型
enum RpcTextType{
	RpcTimeText,	// 时间
	RpcDescText,	// 通道
	RpcSnapText		// 下排抓拍
}

// 视频流分辨率
enum RpcStreamResolution{
	RPC_FHD = 0,	// 1920*1080
	RPC_UXGA = 1,	// 1600*1200
	RPC_XGA = 2,	// 1024*768
	RPC_VGA = 3,	// 640*480
	RPC_HD = 4	// 1280*720
}

// 视频流中人脸大小
enum RpcTargetSize{
	RPC_TAR_SMALL = 0,
	RPC_TAR_MIDDLE = 1,
	RPC_TAR_LARGE = 2,
}

// OSD字体对齐方向
enum RpcTextAlignType{
	RPC_UPPERLEFT_ALIGN,
	RPC_LOWERLEFT_ALIGN,
	RPC_UPPERRIGHT_ALIGN,
	RPC_LOWERRIGHT_ALIGN
}

// 图传图片格式
enum RpcImgFormat{
	RPC_JPEG = 0
}

// 智能视频流类型
enum RpcSmartStreamType{
	RPC_SINGLESTREAM_SNAPONTOP = 0,	// 人脸墙在顶部
	RPC_SINGLESTREAM_SNAPONBOTTOM = 1,	// 人脸墙在下方
	RPC_SINGLESTREAM_NOSNAP = 2	// 无人脸墙
}

// 去畸变广角图片类型
enum RpcUndistortImgType{
	RPC_UNDISTORT_1080P = 0,
	RPC_UNDISTORT_720P = 1,
	RPC_UNDISTORT_540P = 2,
	RPC_UNDISTORT_CROP = 3
}

// 通讯异常定义
exception RpcLibraFException {
  1: RpcLibraFErrorType err_type,
  2: string msg,
}

// 点位置（归一化[0,1]）
/** a point's coordinates (x, y) are ratios w.r.t. the image width and height **/ 
struct RpcPoint {
  1: double x = 0.5,
  2: double y = 0.5,
}

// 无用
// absolution resolution
struct RpcResolution {
  1: i32 width = 0,
  2: i32 height = 0, 
}

// 四边形, normalized to [0, 1)
struct RpcRect {
  1: double x = 0,
  2: double y = 0,
  3: double width = 0,
  4: double height = 0,
}

// 设置检测ROI(无用)
struct RpcGrid {
  1: RpcRect roi,
  2: i32 rows = 1,
  3: i32 cols = 1,
}

// 设置相机属性
struct RpcSensorProp {
  1: RpcResolution resolution,
  2: double exposure = 1,
  3: bool exposure_auto = true,
  4: double shutter = 0.01,
  5: bool shutter_auto = false,
  6: double fps = 20,
  7: bool fps_auto = false,
}

// 电机属性结构体
struct RpcMotorProp {
  1: RpcMotorMode mode = 1,
  2: double mode_val = 0.05, 
}

// 设置多边形检测区域
struct RpcDetectProp{
  1: list<list<RpcPoint>> polygons,
  2: i32 dist = 50,
  3: double threshold = 0.95,
}

// 设置视频中的分布
struct RpcLayoutProp {
  1: bool default_layout = true,	// 默认分布
  2: bool pip_on = true,	// 开启画中画
  3: bool pip_fixed = true,	//　画中画位置随聚焦位置改变
  4: RpcRect pip_roi,	// 画中画位置
  5: i32 snap_cols = 6,	// 抓拍人脸列数
  6: i32 snap_rows = 1,	//　抓拍人脸行数
}

// 矩阵
struct RpcMat {
  1: binary data,
  2: i32 rows,
  3: i32 cols,
  4: i16 type_size,	// size of the type in byte, 8 for uchar
  5: i16 dims,
}

// 色彩
struct RpcColor {
  1: i16 val0 = 0,
  2: i16 val1 = 0,
  3: i16 val2 = 0,
}

// 设置昼夜切换模式模式
struct RpcDayNightTime {
  1: bool is_auto = false;	//　自动切换（7:00~19:00）
  2: bool is_bw = true;	// 夜间黑白/全彩
  3: i32 start_tm = 1900,	// 黑夜开始时间　hour*100 + min
  4: i32 end_tm = 700,	// 黑夜结束时间　hour*100 + min
}

// 字体属性
struct RpcFontProperties {
	1: string font_filename ="../data/truetype/simsun.ttf",	// 字体文件名
	2: i16 font_size = 20,	//　字体大小
	3: double interval_scale = 0.1,	//　字符间隔
	4: double space_scale = 0.5,	// 空格大小
	5: RpcPoint pos_ll,	// left lower position	距离对齐位置的偏移量
	6: RpcTextAlignType text_align,	// 对其方式
	7: RpcColor font_color,	// 字体颜色　bgr colorspace
	8: RpcColor outline_color,	// 字体边框颜色（无用）　bgr colorspace
	9: bool is_display = true	// 是否显示　if this text will be show on the screen
}

// OSD其他属性
struct RpcOSDOther {
	1: bool is_24hour = true,	// 24小时制
	2: bool show_weekday = true,	// 显示星期
	3: string zh_str = "格灵深瞳人眼相机"	// 通道名
}

// 编码属性
struct RpcStreamProperties {
	1: RpcStreamResolution res,	// 分辨率
	2: bool is_bitrate_variable = false,	// 是否可变码流（不支持可变）
	3: i32 bitrate = 4000,	// 千码率
	4: i16 fps = 20,	// 帧率
	5: i16 kframe_interval = 15,	//　关键帧间隔
}

// 主码流和子码流编码属性
struct RpcTwoStreamProperties {
	// 主码流
	1: RpcStreamResolution main_res,
	2: bool main_bitrate_variable = false,
	3: i32 main_bitrate = 5000,
	4: i32 main_fps = 20,
	5: i32 main_kframe_interval = 100,

	// 子码流
	6: bool sub_bitrate_variable = false,
	7: i32 sub_bitrate = 1000,
	8: i32 sub_fps = 20,
	9: i32 sub_kframe_interval = 100,
	10: bool is_sub_on = true,
}

// 图传属性
struct RpcImgTransProperties {
	1: RpcImgFormat format,	// 图片格式
	2: string ip = "127.0.0.1",	//　接受端ip
	3: i16 port = 9900,	// 接受端端口
	4: bool is_snap_trans = true, // 是否传输抓拍
	5: bool is_fovea_trans = false,	// 是否传输相应长焦图
}

struct RpcSnapProps {
	1: map<RpcSnapType, RpcImgTransProperties> snap_props,
	2: i16 server_port,
}

struct RpcSnapConnectInfo {
	1: i16 num_cur_connect = 0,	// 当前连接数
	2: i16 num_max_connect = 2,	// 最大连接数
}

service LibraFService{
   
   void Stop() throws (1:RpcLibraFException excpt),
   
   // work mode services
   /** 获取工作模式　get work mode **/
   RpcWorkMode GetWorkMode() throws (1:RpcLibraFException excpt),
   /** 设置工作模式　set work mode, return false if failed to switch work mode **/
   void SetWorkMode(1:RpcWorkMode work_mode) throws (1:RpcLibraFException excpt),
   /** 切换到手动模式，一段时间不进行操作则自动切回自动模式　switch to the passive mode, and will be automatically switch back to catchall mode if no more controll has been send to libraf **/
   void SwitchToPassiveModeWithTimer() throws (1:RpcLibraFException excpt),
   /** 系统是否正忙　if system is blocked to recieve any commend from client **/
   bool IsBlocking();
   
   // 开关红外滤光片　IRCut　
   /** close the IRcut (ir will be filtered), if is_ir_on is true **/
   void SetIRCut(1:bool is_ir_on) throws (1:RpcLibraFException excpt),
   /** get true if the IRcut is close (ir is filtered) **/
   bool GetIRCut() throws (1:RpcLibraFException excpt),
   void SetDayNight(1:RpcDayNightTime interval) throws (1:RpcLibraFException excpt),
   RpcDayNightTime GetDayNight() throws (1:RpcLibraFException excpt),
   
   // 图传配置　image tranfer
   /** 获取长焦/广角小尺寸图　get a encoded frame as a string from the wide view or the long focus camera **/
   RpcMat GetRawImg(1:RpcSensorType sensor_type) throws (1:RpcLibraFException excpt),
   /** 获取视频流图片　get a encoded frame as a string of the video stream **/
   RpcMat GetStreamImg() throws (1:RpcLibraFException excpt),
   /** 获取长焦/广角原尺寸图　get a encoded jpeg image with original size from the wide view or the long focus camera **/
   RpcMat GetFullSzRawImg(1:RpcSensorType sensor_type) throws (1:RpcLibraFException excpt),
   /** 获取广角去畸变　get a undistort frame from wide camera**/
   RpcMat GetUndistortWideImg(1:RpcUndistortImgType undistort_type) throws (1:RpcLibraFException excpt),
   
   // 相机配置　sensor services
   /** get sensor properties **/
   RpcSensorProp GetSensorProperties(1:RpcSensorType sensor_type) throws (1:RpcLibraFException excpt),
   /** set sensor properties, return false if failed to set sensor properties **/
   void SetSensorProperties(1:RpcSensorType sensor_type, 2:RpcSensorProp sensor_prop) throws (1:RpcLibraFException excpt),
   /** 设置相机光圈电压值　**/
   void SetIrisOffset(1:RpcSensorType sensor_type, 2:i32 offset) throws (1:RpcLibraFException excpt),
   i32 GetIrisOffset(1:RpcSensorType sensor_type) throws (1:RpcLibraFException excpt),
	
   // 电机控制　motor services
   /** 未实现　get motor properties **/
   RpcMotorProp GetMotorProperties() throws (1:RpcLibraFException excpt),
   /** 未实现　set motor properties, return false if failed to set motor properties **/
   void SetMotorProperties(1:RpcMotorProp motor_prop) throws (1:RpcLibraFException excpt),
   // unavailable to control motor while calibration or under the RPC_CORE_CATCHALL_WORKMODE mode
   /** 在视频流上指哪打哪　look at the point refer to the streaming coordinate system **/
   void SetLookAtPointOnStream(1:RpcPoint point) throws (1:RpcLibraFException excpt),
   /** 在广角画面中移动聚焦位置　move the look at point with the vector "RpcPoint& point" refer to the streaming coordinate system **/
   void MoveLookAtPointOnStream(1:RpcPoint point) throws (1:RpcLibraFException excpt),
   /** 在广角画面上指哪打哪　look at the point refer to the original image coordinate system **/
   void SetLookAtPoint(1:RpcPoint point) throws (1:RpcLibraFException excpt),
   /** 直接控制电机（输入单位为电机编码器精度）　directly rotate the view of long focus camera **/
   void RotateMotorSmallStep(1:RpcRotateType rot_type, 2:i32 nsteps) throws (1:RpcLibraFException excpt),
   /** 直接控制电机（输入单位为预定大小）　directly rotate the view of long focus camera **/
   void RotateMotorWithGivenStepLevel(1:RpcRotateType rot_type, 2:RpcRotateStep level) throws (1:RpcLibraFException excpt),
   /** 转动至初始位置　Reset the motor to the original position **/
   void ResetMotor() throws (1:RpcLibraFException excpt),
   
   // 码流控制　streaming services
   /** set layout properties **/
   void SetLayoutProperties(1:RpcLayoutProp layout_prop) throws (1:RpcLibraFException excpt),
   /** get layout properties **/
   RpcLayoutProp GetLayoutProperties() throws (1:RpcLibraFException excpt),
   /** set/get the type of smart streaming properties **/
   void SetSmartStreamType(1:RpcSmartStreamType smart_stream_type) throws (1:RpcLibraFException excpt),
   RpcSmartStreamType GetSmartStreamType() throws (1:RpcLibraFException excpt),
   /** 无用　set streaming properties **/
   void SetStreamProperties(1:RpcStreamType stream_type, 2:RpcStreamProperties stream_prop) throws (1:RpcLibraFException excpt),
   /** 无用　get streaming properties **/
   RpcStreamProperties GetStreamProperties(1:RpcStreamType stream_type) throws (1:RpcLibraFException excpt),
   /** set both streaming properties **/
   void SetTwoStreamProperties(1:RpcTwoStreamProperties stream_prop) throws (1:RpcLibraFException excpt),
   /** get both streaming properties **/
   RpcTwoStreamProperties GetTwoStreamProperties() throws (1:RpcLibraFException excpt),
   
   
   // 检测配置　detection services
   // 检测区域
   /** set detection properties, throw error if failed to set detection properties **/
   void SetDetectionProperties(1:RpcDetectProp det_roi) throws (1:RpcLibraFException excpt),
   /** get detection properties **/
   RpcDetectProp GetDetectionProperties() throws (1:RpcLibraFException excpt),
   // 图像遮盖（相应区域不检测且填充为黑）
   /** set image masks, false mask is over the boundary of image **/
   void SetImageMasks(1:list<list<RpcPoint>> img_masks) throws (1:RpcLibraFException excpt),
   /** get detection properties **/
   list<list<RpcPoint>> GetImageMasks() throws (1:RpcLibraFException excpt),
   /** 打开图像遮盖功能　image masks will be implemented if is_mask_on is true **/
   void SetMaskOn(1:bool is_mask_on) throws (1:RpcLibraFException excpt),
   /** 获取图像遮盖功能状态　get true if image masks has been implemented **/
   bool GetMaskOn() throws (1:RpcLibraFException excpt),
   
   // 自动校准　calibration services
   /** do calibration includes two modes: 
   1. (is_auto = true) automatically align centers and calibrate
   2. (is_auto = false) automatically calibrate but munually align centers throught SetLookAtPoint before implementation of it **/
   void Calibrate(1:bool is_auto) throws (1:RpcLibraFException excpt),
   /** 中断自动校准　force to stop calibration: **/
   void StopCali() throws (1:RpcLibraFException excpt),
   /** 是否正在自动校准　if calibration is running **/
   bool CaliBusy() throws (1:RpcLibraFException excpt),
   /** 校准完成进度　read the completeness of calibration (0 - 100), -1 denotes failed **/
   i32 CaliState() throws (1:RpcLibraFException excpt),
   /** 校准开始前长焦画面应当在广角画面中的位置　get the roi of the wide view into which the long view should be aligned **/
   RpcRect GetAlignROI() throws (1:RpcLibraFException excpt),
   
   // 背景学习（功能定义还需讨论）　BGM services
   /** learn BGM **/
   void LearnBGM() throws (1:RpcLibraFException excpt),
   /** read the completeness of learning bgm (0 - 100) **/
   i32 LearnBGMState() throws (1:RpcLibraFException excpt),
   /** get BGM sensitivity **/
   double GetBGMSensitivity() throws (1:RpcLibraFException excpt),
   /** set BGM sensitivity, return false if failed to set sensitivity (0-255 float)**/
   void SetBGMSensitivity(1:double sen) throws (1:RpcLibraFException excpt),
   
   // OSD
   // 配置字体
   void SetFontProperties(1:RpcTextType text_type, 2:RpcFontProperties font_prop) throws (1:RpcLibraFException excpt),
   RpcFontProperties GetFontProperties(1:RpcTextType text_type) throws (1:RpcLibraFException excpt),
   /** set the status of other display details (24-hour time, show display and channel string) **/
   void SetOSDOthers(1:RpcOSDOther osd_other) throws (1:RpcLibraFException excpt),
   /** get the status of other display details (24-hour time, show display and channel string) **/
   RpcOSDOther GetOSDOthers() throws (1:RpcLibraFException excpt),
   // 配置对齐
   /** set the type of text alignment **/
   void SetTextAlign(1:RpcTextType text_type, 2:RpcTextAlignType align_type) throws (1:RpcLibraFException excpt),
   /** get the type of text alignment **/
   RpcTextAlignType GetTextAlign(1:RpcTextType text_type) throws (1:RpcLibraFException excpt),
   
   // 视频其他
   /** 在视频中画出检测框 **/
   void SetDrawBBS(1:bool is_draw_bbs_) throws (1:RpcLibraFException excpt),
   bool GetDrawBBS() throws (1:RpcLibraFException excpt),
   void SetDrawView(1:bool is_draw_view_) throws (1:RpcLibraFException excpt),
   bool GetDrawView() throws (1:RpcLibraFException excpt),
   void SetDrawDetGrid(1:bool is_draw_) throws (1:RpcLibraFException excpt),
   bool GetDrawDetGrid() throws (1:RpcLibraFException excpt),
	
   // 检测控制 
   /** 设置检测功能列表　enable the the corresponding detection tasks **/
   void SetDetTasks(1:list<RpcSnapType> snap_type) throws (1:RpcLibraFException excpt),
   /** get the list of detection tasks **/
   list<RpcSnapType> GetDetTasks() throws (1:RpcLibraFException excpt),
   
   // 图传控制　Snap Control
   void SetSnapProps(1:RpcSnapProps snap_props) throws (1:RpcLibraFException excpt),
   RpcSnapProps GetSnapProps() throws (1:RpcLibraFException excpt),
   RpcSnapConnectInfo GetSnapConnectionInfo() throws (1:RpcLibraFException excpt),
   string GetSnapPublicKey() throws (1:RpcLibraFException excpt),
   string ResetSnapPriveteKey() throws (1:RpcLibraFException excpt),
   void SetCompatible(1:bool compatible) throws (1:RpcLibraFException excpt),
   bool GetCompatible() throws (1:RpcLibraFException excpt),
   
   
   /** set the img transfer properties **/
   void SetImgTransProperties(1:RpcSnapType snap_type, 2:RpcImgTransProperties img_trans_prop) throws (1:RpcLibraFException excpt),
   /** get the img transfer properties **/
   RpcImgTransProperties GetImgTransProperties(1:RpcSnapType snap_type) throws (1:RpcLibraFException excpt),
   /** 配置图传类型列表　enable the img transfer task of the corresponding tasks **/
   void SetImgTransList(1:list<RpcSnapType> snap_type) throws (1:RpcLibraFException excpt),
   /** get the list img transfer tasks **/
   list<RpcSnapType> GetImgTransList() throws (1:RpcLibraFException excpt),
   
   
   // process the parameters　（目前无需外部控制）
   /** save to local file **/
   void SaveParam() throws (1:RpcLibraFException excpt),
   /** read from local file **/
   void LoadParam() throws (1:RpcLibraFException excpt),
   
   // start/stop libraf_main
   // 无用
   void StartLibraF() throws (1:RpcLibraFException excpt),
   // 安全关闭（重启）程序
   void StopLibraF() throws (1:RpcLibraFException excpt),
}
