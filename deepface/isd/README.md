老版face系统中isd通过zmq方式接收F相机的图传，调matrix相关接口，对图片中目标进行质量过滤

新版face系统中增加importer模块，可通过zmq和ftp等方式接收图片流，然后通过kafka将数据推给isd，isd调matrix相关接口，对图片中目标进行质量过滤

