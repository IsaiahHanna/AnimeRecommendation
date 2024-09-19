library(tidyverse)
library(readxl)
setwd("C:\\Users\\isaia\\OneDrive\\Personal Datasets\\Anime Recommendation")
anime <- read_excel("animes.xls")
anime_ordered <- arrange(anime,ranked)
head(anime_ordered)
for (i in length(anime_ordered)){
  if (anime_ordered[i] == anime_ordered[i+1]){
    anime_ordered <- anime_ordered[-c(i),]
  }
}
