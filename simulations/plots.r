n = 1000
m = 1000
s = 2

fn = 'results/performance.csv'
performance = read.csv(fn, header=F, colClasses='numeric')
performance_jgc = c(0.6249, 1.7958, 51.4000, 1871.5, 20596, NA, NA)
#pdf('results/performance.pdf')
png('results/performance.png', width=800,height=700,res=172)
par(mar=c(5,5,2,2))
matplot(performance[,1], cbind(performance[,2:3], performance_jgc) , type='o', xlab='n', ylab='time (sec)', pch=15:17, col=c('green','red', 'blue'), cex=1.5,cex.axis=1.5, cex.lab=2, lwd=2, log='xy')
legend('topleft', c('tree-based RT', 'naive RT', 'EC'), lty=1:3, pch=15:17, col=c('green', 'red', 'blue'), lwd=2, cex=1.5)
dev.off()

fn = 'data/position.clickcnts.loggedin.csv'
data = read.csv(fn, header=F, colClasses='numeric')
rank = data[,2] + 1
click_cnts = data[,1]
indexes = rank > -1 
#pdf('results/click_distribution.pdf')
png('results/click_distribution.png', width=800,height=700,res=172)
par(mar=c(6,5,2,2))
plot(rank[indexes], click_cnts[indexes], log='xy', xlab='search rank', ylab='# clicks', pch=16, cex=1.5,cex.axis=1.5, cex.lab=2)
dev.off()

#library(igraph)
#clicks = rep(rank, click_cnts)
#power.law.fit(clicks)

#library(VGAM)
#pos_max = 1000
#y = (1: pos_max)
#fit = vglm (y ~ 1, zipf(link=identity, init=2), tra=TRUE, weight=click_cnts[1:pos_max])
#> Coef(fit)
#       s 
#1.349517 

#fn = paste('results/accuracy.n', n, '.m', m, '.s', s, '.csv', sep='')
#accuracy = read.csv(fn, header=F, colClasses='numeric')
#pdf('results/accuracy.pdf')
#plot(accuracy[,1], accuracy[,2], xlab='budget', ylab='total value', pch=16)
#dev.off()

fn = 'results/approximation.csv'
errors = read.csv(fn, header=F, colClasses='numeric')
errors_jgc = rep(0, dim(errors)[1])
#pdf('results/accuracy.pdf')
png('results/approximation.png', width=800,height=700,res=172)
par(mar=c(5,5,2,2))
matplot(errors[,1], cbind(errors[,2:3], errors_jgc), type='o', xlab=expression(alpha), ylab='RSME', pch=15:17, log='x', cex=1.5,cex.axis=1.5, cex.lab=2, lwd=2, col=2:4)
legend('right', c('RT ranking', 'assortative ranking', 'EC ranking'), lty=1:3, pch=15:17, lwd=2, cex=1.5, col=2:4)
dev.off()