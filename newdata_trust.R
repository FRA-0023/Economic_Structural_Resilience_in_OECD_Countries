rm(list=ls())
setwd("C:\\Users\\3003f\\Downloads")
load("extval2.rda")
ead2019s <- names(ead2019); ead2019s

library(dplyr)

ead <- ead2019 %>%
  select(country, year, `Approval_Not_Smoothed`)

write.csv(ead, "ead_selected.csv", row.names = FALSE)



