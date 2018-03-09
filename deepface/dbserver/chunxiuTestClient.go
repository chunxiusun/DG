package main

import (
	"encoding/json"
	"flag"
	"fmt"

	//"github.com/deepglint/ark/dbserver/dbcache"
	"github.com/deepglint/ark/dbserver/models"
	//"github.com/deepglint/ark/dbserver/services"
	"github.com/deepglint/util/random"
	"github.com/golang/glog"
	"golang.org/x/net/context"
	"google.golang.org/grpc"
)
/*
var (
	ds        services.databaseService
	ds_hanyun services.databaseService
	redisaddr map[string]string
	cachecfg  map[string]config.CacheSqlConfig
)

func init() {
	config.SetConfigFile("./../config.json")
	redisConn, _ := dbcache.NewDBCacheInterface()
	ds = NewDatabaseService(redisConn)
	resp, err := ds.ExecuteSql(context.Background(), &models.SqlRequest{
		SqlStr: "create table if not exists test (v1 text, v2 text);",
	})
	if err != nil {
		t.Log(err)
		return
	}

}
*/

func main() {
	flag.Parse()

	conn, err := grpc.Dial("192.168.2.162:8041", grpc.WithInsecure())
	if err != nil {
		glog.Fatalf("fail to dial: %v", err)
		return
	}
	ctx := context.Background()
	client := models.NewDatabaseServiceClient(conn)

	metaBatchInsert := &models.BatchMetaInsert{Table: "test"}
	multiFileds := make([][]*models.Field, 0)
	/*for i := 0; i < 5; i++ {
		fields := make([]*models.Field, 0)
		for j := 1; j < 3; j++ {
			fields = append(fields, &models.Field{Key: fmt.Sprintf("v%d", j), Value: random.RandSeq(10)})
		}
		multiFileds = append(multiFileds, fields)
	}*/
        fileds = append(fields,&models.Field{Key: "ts", Value: 150234543337})
        fileds = append(fields,&models.Field{Key: "sensor_id", Value: "214bbdbc-3d5c-4abb-9349-7b97e163e1ff"})
        fileds = append(fields,&models.Field{Key: "face_id", Value: "1234567"})
        fileds = append(fields,&models.Field{Key: "face_reid", Value: "1234567"})
        fileds = append(fields,&models.Field{Key: "feature", Value: "1234567"})
        fileds = append(fields,&models.Field{Key: "confidence", Value: 0.85})
        fileds = append(fields,&models.Field{Key: "gender_id", Value: 0})
        fileds = append(fields,&models.Field{Key: "gender_confidence", Value: 0})
        fileds = append(fields,&models.Field{Key: "age_id", Value: 0})
        fileds = append(fields,&models.Field{Key: "age_confidence", Value: 0})
        fileds = append(fields,&models.Field{Key: "nation_id", Value: 0})
        fileds = append(fields,&models.Field{Key: "nation_confidence", Value: 0})
        fileds = append(fields,&models.Field{Key: "glass_id", Value: 0})
        fileds = append(fields,&models.Field{Key: "glass_confidence", Value: 0})
        fileds = append(fields,&models.Field{Key: "image_uri", Value: "1"})
        fileds = append(fields,&models.Field{Key: "thumbnail_image_uri", Value: "1"})
        fileds = append(fields,&models.Field{Key: "cutboard_image_uri", Value: "1"})
        fileds = append(fields,&models.Field{Key: "cutboard_x", Value: 1})
        fileds = append(fields,&models.Field{Key: "cutboard_y", Value: 1})
        fileds = append(fields,&models.Field{Key: "cutboard_width", Value: 1})
        fileds = append(fields,&models.Field{Key: "cutboard_height", Value: 1})
        fileds = append(fields,&models.Field{Key: "cutboard_res_width", Value: 1})
        fileds = append(fields,&models.Field{Key: "cutboard_res_height", Value: 1})
        fileds = append(fields,&models.Field{Key: "is_warned", Value: 2})
        fileds = append(fields,&models.Field{Key: "status", Value: 1})

	metaBatchInsert.MultiFields = multiFileds
	body, _ := json.Marshal(metaBatchInsert)
	fmt.Println(string(body))

	resp, err := client.ExecuteMeta(ctx, &models.MetaExecuteRequest{
		Tag:      "faces",
		MetaOpts: models.DBOpts_DB_Opts_Batch_Insert,
		MetaBody: body,
	})
	if err != nil {
		glog.Warningln(err)
	}
	glog.Infoln(resp)
	/*
			req := new(models.GetCacheRequest)
			req.CacheId = "rule" //"civil"//"rule" //"sensor"
			// req.GroupId = "c30c616c-23a2-4ea5-a985-db7388d95af6" //"b0cc6802-51ee-4d0e-a4da-b856b65324ee" //"5300"
			req.ValueId = "11ddcd66-2e04-4f51-998b-af22f08a605a" //"90d37cd6-994d-465d-90c5-89dcd3c297ad" //"b0cc6802-51ee-4d0e-a4da-b856b65324ee"
		resp, err := client.GetCachedFieldData(ctx, req)
		if err != nil {
			fmt.Println(err)
		} else {
			glog.Infoln(len(resp.GetFieldData()))
		}

	*/
	// Handle exiting signals and process.
	/*
		sigChan := make(chan os.Signal, 1)
		signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)

		for {
			select {
			case <-sigChan:
				conn.Close()
				et := time.Now()
				glog.Infof("get from %s to %s", st.String(), et.String())
				glog.Infof("get %d cached results within %d millsecond, and %d per second", atomic.LoadInt64(&count), (et.UnixNano()-st.UnixNano())/1000000, atomic.LoadInt64(&count)/(et.Unix()-st.Unix()))
				return
			default:
				time.Sleep(time.Second)
			}
		}
	*/
}
