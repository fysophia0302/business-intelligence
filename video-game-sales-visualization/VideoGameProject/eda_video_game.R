# Visualizations
library(hrbrthemes)
library(gganimate)
library(gapminder)
library(babynames)
library(ggthemes)
library(cowplot)
library(ggplot2)

# Data Manipulation
library(dplyr)
# Statistics
library(DescTools)

if(!require(pacman))install.packages("pacman")

pacman::p_load('dplyr', 'tidyr', 'gapminder',
               'ggplot2',  'ggalt',
               'forcats', 'R.utils', 'png', 
               'grid', 'ggpubr', 'scales',
               'bbplot')
# install.packages('devtools')
devtools::install_github('bbc/bbplot')

#import the dataset
raw_data<-read.csv('E:/DS/repo/project_fy/video game/vgsales.csv')
head(raw_data, 5)

#compute the size of data frame
dim(raw_data)

#compute the "N/A" number
sum(raw_data$Year == "N/A")
#drop the "N/A" rows
w<-which(raw_data$Year=="N/A")
raw_data2<-raw_data[-w,]
dim(raw_data2)

#select the recent 5 years
raw_data_3<-filter(raw_data2,Year>2005,Year<2017)
dim(raw_data_3)


#select and delete outliers
plot(density(raw_data_3$NA_Sales))
boxplot(raw_data_3$NA_Sales)
## get the outliers
out=boxplot(raw_data_3$NA_Sales)$out
out
## get the outliers index
x<-which(raw_data_3$NA_Sales %in% out)
## get the clean data
clean_data<-raw_data_3[-x,]
## check the clean data
boxplot(clean_data$NA_Sales)

dim(clean_data)


#generate the the relationship of platform and sale count
platform <-clean_data %>% 
  group_by(Platform)%>% 
  summarise(Count = n())


ggplot(platform,aes(x = Platform , y = Count,fill=Count)) +
  theme_bw()+
  theme(panel.border = element_blank(),axis.text.x = element_text(angle = 45, hjust = 0.5, vjust = 0.5))+
  geom_col() +
  ggtitle('Platform VS Sale Count')+
  scale_fill_distiller(palette = 'Spectral') +
  ylab('Sale Count')

#generate the the relationship of  different years and count
years <-clean_data %>% 
  group_by(Year)%>% 
  summarise(Count = n())

ggplot(years,aes(x = Year , y = Count,fill=Count)) +
  theme_bw()+
  geom_col() +
  theme(panel.border = element_blank(),axis.text.x = element_text(angle = 45, hjust = 0.5, vjust = 0.5))+
  ggtitle('Year vs Sale Count')+
  scale_fill_distiller(palette = 'Spectral') +
  ylab('Sale Count')+
  xlab('Year')

#generate the the relationship of  different years and percentage
Year_freq<-table(clean_data$Year)
Year_Per<- prop.table(table(clean_data$Year) * 100)
year_df<-data.frame(cbind(Year_freq,Year_Per))
year_df               

ggplot(year_df,aes(x = row.names(year_df) , y = Year_Per,fill=Year_Per)) +
  geom_col()+
  bbc_style() +
  theme_bw()+
  theme(panel.border = element_blank(),axis.text.x = element_text(angle = 45, hjust = 0.5, vjust = 0.5))+
  ggtitle('Year VS Sale Percentage')+
  scale_fill_distiller(palette = 'Spectral') +
  ylab('Percentage')+
  xlab('Year')

#generate the the relationship of different game and percentage
Name_freq<-table(clean_data$Name)
Name_Per<- prop.table(table(clean_data$Name) * 100)
Name_df<-data.frame(cbind(Name_freq,Name_Per))
head(Name_df,10)
Name_df<- head(Name_df[order(Name_df$Name_freq, decreasing = T), ], 10)

ggplot(Name_df,aes(x = row.names(Name_df) , y = Name_Per,fill=Name_Per)) +
  geom_col()+
  bbc_style() +
  theme_bw()+
  theme(panel.border = element_blank(),axis.text.x = element_text(angle = 45, hjust = 0.5, vjust = 0.5))+
  ggtitle('Game Vs Sale Percentage')+
  scale_fill_distiller(palette = 'Spectral') +
  ylab('Percentage')+
  xlab('Game')

#generate the the relationship of different Game and Sale Count
Name_freq<-table(clean_data$Name)
Name_Per<- prop.table(table(clean_data$Name) * 100)
Name_df<-data.frame(cbind(Name_freq,Name_Per))
head(Name_df,10)
Name_df<- head(Name_df[order(Name_df$Name_freq, decreasing = T), ], 10)

ggplot(Name_df,aes(x = row.names(Name_df) , y = Name_freq,fill=Name_freq)) +
  geom_col()+
  bbc_style() +
  theme_bw()+
  theme(panel.border = element_blank(),axis.text.x = element_text(angle = 45, hjust = 0.5, vjust = 0.5))+
  ggtitle('Game Vs Sale Count (Top 10)')+
  scale_fill_distiller(palette = 'Spectral') +
  ylab('Sale Count')+
  xlab('Game Name')

#generate the the relationship of different Publisher and Sale Count
Publisher_freq<-table(clean_data$Publisher)
Publisher_Per<- prop.table(table(clean_data$Publisher) * 100)
Publisher_df<-data.frame(cbind(Publisher_freq,Publisher_Per))
head(Publisher_df,10)
Publisher_df<- head(Publisher_df[order(Publisher_df$Publisher_freq, decreasing = T), ], 10)

ggplot(Publisher_df,aes(x = row.names(Publisher_df) , y = Publisher_freq,fill=Publisher_freq)) +
  geom_col()+
  bbc_style() +
  theme_bw()+
  theme(panel.border = element_blank(),axis.text.x = element_text(angle = 45, hjust = 0.5, vjust = 0.5))+
  ggtitle('Publisher Vs Sale Count (Top 10)')+
  scale_fill_distiller(palette = 'Spectral') +
  ylab('Sale Count')+
  xlab('Publisher')

#generate the the relationship of different Genre and Sale Count
Genre_freq<-table(clean_data$Genre)
Genre_Per<- prop.table(table(clean_data$Genre) * 100)
Genre_df<-data.frame(cbind(Genre_freq,Genre_Per))
head(Genre_df,10)
Genre_df<- head(Genre_df[order(Genre_df$Genre_freq, decreasing = T), ], 10)

ggplot(Genre_df,aes(x = row.names(Genre_df) , y = Genre_freq,fill=Genre_freq)) +
  geom_col()+
  bbc_style() +
  theme_bw()+
  theme(panel.border = element_blank(),axis.text.x = element_text(angle = 45, hjust = 0.5, vjust = 0.5))+
  ggtitle('Genre Vs Sale Count (Top 10)')+
  scale_fill_distiller(palette = 'Spectral') +
  ylab('Sale Count')+
  xlab('Genre')




