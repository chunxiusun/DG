dgvehicle检测效果评测脚本

detectRateMultiple.py：针对12个图片集（视频抽帧），基于人工标注数据与dgvehicle跑出来结果进行比对分析，得出召回率和准确率

draw.py：算法新版本在12个测试集上得出的召回率和准确率与老版本的画图，使得比对效果可视化

drawClassifiy.py：基于dgvehicle跑出来的结果，在图片上画出机动车、非机动车、行人的cutboard，便于可视化分析检测效果

test_dgvehicle.sh：调dgvehicle，跑出模型检测结果
