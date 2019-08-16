#!/usr/bin/env R BATCH

library(cluster)

points <- read.table('points.xy', sep=",")
names(points) <- c('x', 'y')

points.pam <- pam(points, 10)

plot(points$x, points$y, col=points.pam$clustering, main="Convergence test, k=4", cex=0.5, pch=16, xlab="x", ylab="y")
points(points.pam$medoids, pch=15, col=1:5, cex=1.25)

