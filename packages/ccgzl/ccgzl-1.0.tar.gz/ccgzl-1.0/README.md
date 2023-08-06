by:pianshilengyubing
在原有的changecoord基础上增加了gcj02_to_wgs84互相的转换
有以下函数：
bd09mc_to_bd09(self, mercartorX, mercartorY)
bd09_to_bd09mc(self, lng, lat)
gcj02_to_bd09(self, lng, lat)
bd09_to_gcj02(self, lng, lat)
wgs84_to_gcj02(self, lng, lat)
gcj02_to_wgs84(self, lng, lat)
bd09_to_wgs84(self, lng, lat)
wgs84_to_bd09(self, lng, lat)
bd09mc_to_wgs84(self, lng, lat)



