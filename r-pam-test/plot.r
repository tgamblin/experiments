#!/usr/bin/env R BATCH


points <- read.table('foo', sep=",")
names(points) <- c('x', 'y')

plot(points$x, points$y, main="Convergence test, k=4", cex=0.5, pch=16, xlab="x", ylab="y")

