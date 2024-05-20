library(dplyr)
library(tidyr)
library(ggplot2)
library(ggthemes)
library(patchwork)

AUTHORS <- list(
    'abbott1985' = "Abbott 1985",
    'clouse-1997' = "Clouse 1997",
    'daniels2010' = "Daniels 2010",
    'davies_and_comrie1985' = "Davies & Comrie 1985",
    'dutton1970' = "Dutton 1970",
    'dutton2010' = "Dutton2010",
    'dye-et-al-1968' = "Dye et al. 1968",
    'foley2005' = "Foley 2005",
    'franklin1975' = "Franklin 1975",
    'laycock1968' = "Laycock 1968",
    'mcelhanon-1967' = "McElhanon 1967",
    'mcelhanon_and_voorhoeve1970' = "McElhanon & Voorhoeve 1970",
    'scott1978' = "Scott 1978",
    'smallhorn-2011' = "Smallhorn 2011",
    'voorhoeve-1971' = "Voorhoeve 1971",
    'voorhoeve1980' = "Voorhoeve 1980"
)


theme_set(theme_few(base_size=16))
#theme_set(theme_hc(base_size=16))

datasets <- read.csv('datasets.csv', header=TRUE)

res.r <- read.csv('results-recall.csv', header=TRUE) %>% mutate(ID=Dataset)
res.p <- read.csv('results-precision.csv', header=TRUE) %>% mutate(ID=Dataset)
res.f <- read.csv('results-f-scores.csv', header=TRUE) %>% mutate(ID=Dataset)

# rename datasets
res.r$Dataset <- unname(unlist(AUTHORS[res.r$Dataset]))
res.p$Dataset <- unname(unlist(AUTHORS[res.p$Dataset]))
res.f$Dataset <- unname(unlist(AUTHORS[res.f$Dataset]))


res <- rbind(
    res.r %>% gather("Method", "Score", -ID, -Dataset) %>% mutate(Metric = 'Recall'),
    res.p %>% gather("Method", "Score", -ID, -Dataset) %>% mutate(Metric = 'Precision'),
    res.f %>% gather("Method", "Score", -ID, -Dataset) %>% mutate(Metric = 'F-Score')
)

res$Metric <- factor(res$Metric, levels=c('Precision', 'Recall', 'F-Score'))

res[res$Method == 'sca', ]$Method <- 'SCA'
res[res$Method == 'turchin', ]$Method <- 'Turchin'
res[res$Method == 'lexstat', ]$Method <- 'LexStat'
res[res$Method == 'infomap', ]$Method <- 'LexStat+Infomap'
res[res$Method == 'edit', ]$Method <- 'Levenshtein'



res$Method <- factor(res$Method, levels=c('Levenshtein', 'SCA', 'Turchin', 'LexStat', 'LexStat+Infomap'))

p <- ggplot(res, aes(Score, fill=Metric)) +
    geom_histogram() +
    facet_grid(Method~Metric, scales="free") +
    guides(fill="none")

ggsave('figure-accuracy-combined.png', dpi=700)


p <- ggplot(subset(res, Metric == 'F-Score'), aes(Score, fill=Method)) +
    geom_histogram() +
    facet_grid(Method~.) +
    guides(fill="none") +
    scale_x_continuous("F-Score", n.breaks=10)
ggsave('figure-accuracy-fscore.png', dpi=700)



p <- ggplot(
        subset(res, Method=="LexStat+Infomap"),
        aes(Score, Dataset, color=Metric, shape=Metric)
    ) +
    geom_point(size=5, color="#333333") +
    geom_point(size=4) +
    theme(axis.title.y=element_blank())

ggsave('figure-accuracy-infomap.png', dpi=700)


infomap <- res %>% filter(Method=="LexStat+Infomap") %>% left_join(datasets, join_by(ID == Wordlist))

p <- ggplot(infomap, aes(Concepts, Score, color=Dataset)) +
    geom_point() +
    facet_wrap(~Metric, scales="free") +
    guides(color="none")

q <- ggplot(infomap, aes(AverageMutualCoverage, Score, color=Dataset)) +
    geom_point() +
    facet_wrap(~Metric, scales="free") +
    guides(color="none")

ggsave('figure-scatter.png', p / q, dpi=700)


res.p_vs_r <- res.r %>% gather("Method", "Recall", -ID, -Dataset) %>% inner_join(
    res.p %>% gather("Method", "Precision", -ID, -Dataset)
)

res.p_vs_r$Method <- factor(res.p_vs_r$Method, levels=c('edit', 'sca', 'turchin', 'lexstat', 'infomap'))

p <- ggplot(res.p_vs_r, aes(x=Recall, y=Precision, color=Method, shape=Method)) +
    geom_point() +
    facet_wrap(~Dataset, ncol=3) +
    scale_x_continuous(limits=c(0, 1), n.breaks=3) +
    scale_y_continuous(limits=c(0, 1), n.breaks=3) +
    theme(legend.position="top")

ggsave('figure-precision_vs_recall.png', dpi=700)



# List et al.
# \bf Dataset & Turchin&Edit Distance&SCA&LexStat&LS-Infomap\\\hline\hline
# Bahnaric& 0.7397& 0.8537& 0.8568& 0.8804& 0.8813\\\hline
# Chinese& 0.7447& 0.7538& 0.7795& 0.8245& 0.8320\\\hline
# Mabuso& 0.8029& 0.8434& 0.8461& 0.8398& 0.8618\\\hline
# Romance& 0.7505& 0.8288& 0.8943& 0.9050& 0.9185\\\hline
# Tujia& 0.8777& 0.9057& 0.8989& 0.9170& 0.9128\\\hline
# Uralic& 0.9024& 0.8815& 0.8998& 0.9024& 0.9045\\\hline
# \endtabular





res.f <- subset(res, Metric=="F-Score")
res.f <- res.f %>% select(Dataset, Method, Score)

res.f$Study <- 'Greenhill'

res.f <- rbind(res.f, data.frame(
    Dataset = 'List et al. (2017)',
    Method = 'LexStat+Infomap',
    Score = c(
        0.8813,
        0.8320,
        0.8618,
        0.9185,
        0.9128,
        0.9045
    ),
    Study="List et al. (2017)"
))

palette <- scale_fill_viridis_d()$palette(5)

p <- ggplot(subset(res.f, Study=='List et al. (2017)'), aes(Score, y=Method, fill=Method)) +
    geom_vline(xintercept=0.89, color="#DCDCDC", lwd=2) +
    geom_boxplot(alpha=0.9) +
    guides(fill="none") +
    scale_x_continuous("F-Score", limits=c(0, 1), n.breaks=5) +
    scale_fill_manual(values=palette[[5]]) +  # hack
    theme(axis.title.y=element_blank(), axis.title.x=element_blank()) +
    ggtitle("List et al. (2017)")

q <- ggplot(subset(res.f, Study=='Greenhill'), aes(Score, y=Method, fill=Method)) +
    geom_vline(xintercept=0.89, color="#DCDCDC", lwd=2) +
    geom_boxplot(alpha=0.9) +
    guides(fill="none") +
    scale_x_continuous("F-Score", limits=c(0, 1), n.breaks=5) +
    scale_fill_manual(values=palette) +  # hack
    theme(axis.title.y=element_blank()) +
    ggtitle("This Study")



ggsave(filename="figure-boxplot.png", (p / q) +  plot_layout(heights = c(1, 5), guides = 'collect'), width=6, height=4)




palette <- scale_fill_viridis_d()$palette(5)

p <- ggplot(subset(res.f, Study=='Greenhill'), aes(Score, y=Method, fill=Method)) +
    geom_vline(xintercept=0.89, color="#DCDCDC", lwd=1.2) +
    geom_boxplot(alpha=0.9) +
    guides(fill="none") +
    scale_x_continuous("F-Score", limits=c(0, 1), n.breaks=5) +
    scale_fill_manual(values=palette)


ggsave(filename="figure-boxplot-2.png", p, width=6, height=3)

