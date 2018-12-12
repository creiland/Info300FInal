require(dplyr)
require(anytime)
require(ggplot2)
require(plotly)
require(corrplot)

setwd('C:/Users/creil/Desktop/info300final/analysis/')

fifties <- read.csv('data/fifties.csv')
sixties <- read.csv('data/sixties.csv')
sixties <- rbind(six, read.csv('data/sixties_1.csv'), read.csv('data/sixties_2.csv'), read.csv('data/sixties_3.csv'), read.csv('data/sixties_4.csv'))

seventies <- read.csv('data/seventies.csv')
seventies <- rbind(seventies, read.csv('data/seventies_1.csv'), read.csv('data/seventies_2.csv'), read.csv('data/seventies_3.csv'))

eighties <- read.csv('data/eighties.csv')
eighties <- rbind(eighties, read.csv('data/eighties_1.csv'), read.csv('data/eighties_2.csv'), read.csv('data/eighties_3.csv'))

nineties <- read.csv('data/nineties.csv')
nineties <- rbind(nineties, read.csv('data/nineties_1.csv'), read.csv('data/nineties_2.csv'), read.csv('data/nineties_3.csv'))

zeros <- read.csv('data/zeros.csv')
zeros <- rbind(nineties, read.csv('data/zeros_1.csv'), read.csv('data/zeros_2.csv'), read.csv('data/zeros_3.csv'))

big_data <- rbind(fifties, sixties, seventies, eighties, nineties, zeros)
big_data <- na.omit(big_data)

big_data$date <- anydate(as.character(big_data$date))

big_data$year <- lubridate::year(big_data$date)

big_data <- big_data %>%  filter(valence < 1.0)

MaxTable <- function(x){
  dd <- unique(x)
  dd[which.max(tabulate(match(x,dd)))]
}

#averages by year
valence_by_year <- big_data %>% group_by(year) %>% summarise(avg_v = mean(valence))
tempo_by_year <- big_data %>% group_by(year) %>% summarise(avg_t = mean(tempo))
dance_by_year <- big_data %>% group_by(year) %>% summarise(avg_d = mean(danceability))
energy_by_year <- big_data %>% group_by(year) %>% summarise(avg_e = mean(energy))
genre_by_decade <- big_data %>% group_by(decade) %>% summarise(genre = MaxTable(genre))

fifties$decade <- 1950
sixties$decade <- 1960
seventies$decade <- 1970
eighties$decade <- 1980
nineties$decade <- 1990
zeros$decade <- 2000

valence_by_decade <- big_data %>% group_by(decade) %>% summarise(avg_v = mean(valence))

v  <- plot_ly(
  x = valence_by_decade$decade,
  y = valence_by_decade$avg_v,
  name = "Positivity By year",
  type = "bar"
)

v_line <- plot_ly(valence_by_year, x = ~year, y = ~avg_v, type = 'scatter', mode = 'lines') %>% 
  layout(title = "Average Positivity by Year",
         xaxis = list(title = "Year"),
         yaxis = list (title = "Average Valence"))

dance_line <- plot_ly(dance_by_year, x = ~year, y = ~avg_d, type = 'scatter', mode = 'lines') %>% 
  layout(title = "Average Danceability by Year",
         xaxis = list(title = "Year"),
         yaxis = list (title = "Average Danceability"))

tempo_line <- plot_ly(tempo_by_year, x = ~year, y = ~avg_t, type = 'scatter', mode = 'lines') %>% 
  layout(title = "Average Tempo by Year",
         xaxis = list(title = "Year"),
         yaxis = list (title = "Average Tempo"))

energy_line <- plot_ly(energy_by_year, x = ~year, y = ~avg_e, type = 'scatter', mode = 'lines') %>% 
  layout(title = "Average Song Energy by Year",
         xaxis = list(title = "Year"),
         yaxis = list (title = "Average Energy"))


#Events
#sixties
sixties <- na.omit(sixties)
cuban <- na.omit(read.csv('data/cuban_missle.csv'))
c <- t.test(sixties$valence, cuban$valence, var.equal = TRUE)

jfk <- na.omit(read.csv('data/JFK.csv'))
j <- t.test(sixties$valence, jfk$valence, var.equal = TRUE)

mlk <- na.omit(read.csv('data/MLK.csv'))
m <- t.test(sixties$danceability, mlk$danceability, var.equal = TRUE)

summer <- na.omit(read.csv('data/love.csv'))
'%!in%' <- function(x,y)!('%in%'(x,y))
sixties_test <- sixties %>% filter(spotifyID %!in% summer$spotifyID)
s <- t.test(sixties$danceability, summer$danceability, var.equal = TRUE)

m_data <- big_data %>% select(energy, rank, valence, danceability, tempo, year)
matrix = cor(m_data, use = "pairwise.complete.obs")
corrplot(matrix, type = "upper", order = "hclust", 
         tl.col = "black", tl.srt = 60)


nine <- na.omit(read.csv('data/nine11.csv'))
n <- t.test(zeros$danceability, nine$danceability, var.equal = TRUE)

seventies <- filter(seventies, valence <= 1.0)

end_v <- na.omit(read.csv('v_end.csv'))
end <- t.test(seventies$danceability, end_v$danceability, var.equal = TRUE)

end_v <- na.omit(read.csv('v_end.csv'))
end_v <- t.test(seventies$valence, end_v$valence, var.equal = TRUE)

eighties <- filter(eighties, valence <= 1.0)

berlin <- na.omit(read.csv('berlin.csv'))
b_d <- t.test(eighties$danceability, berlin$danceability, var.equal = TRUE)

black <- na.omit(read.csv('black_monday.csv'))
black_d <- t.test(eighties$valence, black$valence, var.equal = TRUE)

nineties <- nineties %>% filter(valence <= 1.0)

columbine <- na.omit(read.csv('columbine.csv'))
co <- t.test(nineties$danceability, columbine$danceability, var.equal = TRUE)


zeros <- zeros %>% filter(valence <= 1.0)
bee <- na.omit(read.csv('data/bee_movie.csv'))
beez <- t.test(zeros$valence, columbine$valence, var.equal = TRUE)


fit_full_rw = lm(rank~., data=m_data)
fit_null_rw = lm(rank~1, data=m_data)
F_fit_rw = step(fit_null_rw, scope=list(lower=fit_null_rw,upper=fit_full_rw),
                direction="forward")

summary(F_fit_rw)

dist <- ggplot(big_data, xlab="valence", ylab='Density', 
                       main='Distribution of Valence', aes(x=energy)) + 
  geom_density() +
  geom_vline(aes(xintercept = mean(big_data$danceability), color = 'Mean'), linetype="dashed") +
  geom_vline(aes(xintercept = median(big_data$danceability), color = 'Median'), linetype="dashed") +
  scale_color_manual(name = "Legend", values = c(Mean = "red", Median = "blue"))
