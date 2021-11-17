library(ggplot2)
library(dplyr)
library(maps)
library(mapproj)
library(dbscan)
library(maptools)

path="~/NER/comparison/"
setwd(paste0(path,"ghewond"))
filelist = list.files(pattern="*.csv$")

df_input_list <- lapply(filelist, fread)
names(df_input_list) <- gsub(filelist, pattern="\\..*", replacement="")
df_merged <-rbind.fill(df_input_list, .id = "id")
data<- df_merged[!is.na(df_merged$lat),]

kNNdistplot(subset(data, select=c(lon,lat)), k = 30)
abline(h=5, col = "red", lty=2)

clusters <- dbscan(select(data, lat, lon), eps =10, minPts=30)
data$cluster <- clusters$cluster


groups  <- data %>% filter(cluster != 0)
noise  <- data %>% filter(cluster == 0)

world <- map_data("world")

p<- ggplot(groups, aes(x = lon, y = lat)) +
  geom_map(data = world, map = world,
           aes(long, lat, map_id = region),color = "darkgrey", fill = "lightgray", size = 0.1)+
  geom_point(aes(fill = "black"), noise, size=0.2) +
  geom_point(aes(colour = as.factor(cluster)), groups,size = 0.6)

show(p)
