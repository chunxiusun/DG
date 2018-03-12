#!/usr/bin/python
# -*- coding:utf-8 -*-

# author : chunxiusun


class LibrafApi():
    def set_get_WorkMode(self,client,work_mode):
	client.SetWorkMode(work_mode)
	resp = client.GetWorkMode()
	return resp

    def switchToPassiveModeWithTimer(self,client):
	client.SwitchToPassiveModeWithTimer()

    def get_set_FontProperties(self,client,text_type,font_prop):
        client.SetFontProperties(text_type,font_prop)
        resp = client.GetFontProperties(text_type)
        return resp

    def get_set_OSDOthers(self,client,osd_other):
	client.SetOSDOthers(osd_other)
	resp = client.GetOSDOthers()
	return resp

    def get_set_TextAlign(self,client,text_type,align_type):
	client.SetTextAlign(text_type,align_type)
	resp = client.GetTextAlign(text_type)
	return resp

    def get_set_ImageMasks(self,client,img_masks):
	client.SetImageMasks(img_masks)
	resp = client.GetImageMasks()
	return resp

    def get_set_MaskOn(self,client,is_mask_on):
	client.SetMaskOn(is_mask_on)
	resp = client.GetMaskOn()
	return resp

    def get_set_LayoutProperties(self,client,layout_prop):
	client.SetLayoutProperties(layout_prop)
	resp = client.GetLayoutProperties()
	return resp

    def get_set_SensorProperties(self,client,sensor_type,sensor_prop):
	client.SetSensorProperties(sensor_type,sensor_prop)
	resp = client.GetSensorProperties(sensor_type)
	return resp
 
    def get_set_DayNight(self,client,interval):
	client.SetDayNight(interval)
        resp = client.GetDayNight()
	return resp

    def get_set_DetectionProperties(self,client,det_roi):
	client.SetDetectionProperties(det_roi)
        resp = client.GetDetectionProperties()
	return resp

    def get_set_ImgTransProperties(self,client,snap_type,img_trans_prop):
	client.SetImgTransProperties(snap_type,img_trans_prop)
        resp = client.GetImgTransProperties(snap_type)
	return resp

    def get_set_ImgTransList(self,client,snap_type):
	client.SetImgTransList(snap_type)
        resp = client.GetImgTransList()
	return resp

    def get_set_DetTasks(self,client,snap_type):
	client.SetDetTasks(snap_type)
        resp = client.GetDetTasks()
	return resp
    def get_set_BGMSensitivity(self,client,sen):
	client.SetBGMSensitivity(sen)
        resp = client.GetBGMSensitivity()
	return resp

    def learnBGM(self,client):
	client.LearnBGM()

    def learnBGMState(self,client):
	resp = client.LearnBGMState()
	return resp
	
    def autoCalibrate(self,client,is_auto):
	client.Calibrate(is_auto)#False or True

    def stopCalibrate(self,client):
	client.StopCali()

    def caliBusy(self,client):
	cali_busy = client.CaliBusy()
	return cali_busy

    def caliState(self,client):
	cali_state = client.CaliState()
	return cali_state

    def isBlocking(self,client):
	is_blocking = client.IsBlocking()
	return is_blocking

    def getAlignROI(self,client):
	resp = client.GetAlignROI()
	return resp

    def setLookAtPointOnStream(self,client,point):
	client.SetLookAtPointOnStream(point)

    def moveLookAtPointOnStream(self,client,point):
	client.MoveLookAtPointOnStream(point)

    def setLookAtPoint(self,client,point):
	client.SetLookAtPoint(point)

    def rotateMotorWithGivenStepLevel(self,client,rot_type,level):
	client.RotateMotorWithGivenStepLevel(rot_type,level)

    def getRawImg(self,client,sensor_type):
	resp = client.GetRawImg(sensor_type)
	return resp

    def getStreamImg(self,client):
	resp = client.GetStreamImg()
	return resp

    def getFullSzRawImg(self,client,sensor_type):
	resp = client.GetFullSzRawImg(sensor_type)
	return resp

    def get_set_TwoStreamProperties(self,client,stream_prop):
	client.SetTwoStreamProperties(stream_prop)
        resp = client.GetTwoStreamProperties()
	return resp

    def get_set_IrisOffset(self,client,sensor_type,offset):
        client.SetIrisOffset(sensor_type,offset)
        resp = client.GetIrisOffset(sensor_type)
        return resp

    def get_set_SmartStreamType(self,client,smart_stream_type):
	client.SetSmartStreamType(smart_stream_type)
	resp = client.GetSmartStreamType()
	return resp

    def getUndistortWideImg(self,client,undistort_type):
	resp = client.GetUndistortWideImg(undistort_type)
	return resp

    def get_set_DrawBBS(self,client,is_draw_bbs):
	client.SetDrawBBS(is_draw_bbs)
	resp = client.GetDrawBBS()
	return resp

    def get_set_DrawView(self,client,is_draw_view):
	client.SetDrawView(is_draw_view)
	resp = client.GetDrawView()
	return resp

    def get_set_SnapProps(self,client,snap_props):
	client.SetSnapProps(snap_props)
	resp = client.GetSnapProps()
	return resp

    def getSnapConnectInfo(self,client):
	resp = client.GetSnapConnectionInfo()
	return resp

    def getSnapPublicKey(self,client):
	resp = client.GetSnapPublicKey()
	return resp

    def resetSnapPriveteKey(self,client):
	resp = client.ResetSnapPriveteKey()
	return resp

    def get_set_Compatible(self,client,compatible):
	client.SetCompatible(compatible)
	resp = client.GetCompatible()
	return resp

    def get_set_DrawDetGrid(self,client,is_draw):
	client.SetDrawDetGrid(is_draw)
	resp = client.GetDrawDetGrid()
	return resp

if __name__ == '__main__':
    pass
