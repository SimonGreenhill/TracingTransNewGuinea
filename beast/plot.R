library(ape)
library(treeio)
library(ggplot2)
library(ggtree)
library(dplyr)

tree <- treeio::read.beast("transnewguinea_combined.mcct.trees")

details <- read.csv('transnewguinea_combined.infomap.csv', header=TRUE)

# remove duplicates
details <- details %>% select(Language, Glottocode, Family, Clade) %>%
    distinct() %>%
    filter(Language %in% tree@phylo$tip.label)


p <- ggtree(tree) + geom_tiplab(aes(label=label))

for (clade in unique(details$Clade)) {
    members <- subset(details, Clade == clade)
    monophy <- is.monophyletic(tree@phylo, members$Language)

    if ((nrow(members) > 1) & monophy) {
        node <- getMRCA(tree@phylo, members$Language)
        p <- p %>% ggtree::collapse(
            node,
            'max',
            fill='steelblue',
            alpha=0.8,
            clade_name=clade,
            color="#333333")
        p <- p + geom_cladelab(
            node=node, label=clade, align=TRUE, #offset = .2,
            textcolor='blue', barcolor='blue')


    } else if (nrow(members) == 1) {
        cat(paste("singleton", clade, "\n"))
    } else {
        cat(paste('not monophyletic:', clade, "\n"))
    }
}

p <- p + scale_x_ggtree() + xlim(0, 0.07)
