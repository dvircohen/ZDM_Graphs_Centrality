# import modules & set up logging
from __future__ import print_function

import gensim


def testing_gensim(sentences):

    # create the model
    model = gensim.models.Word2Vec(sentences, size=10,
                                   alpha=0.025,
                                   min_alpha=0.0001,
                                   sg=1,
                                   iter=10000,
                                   window=5,
                                   cbow_mean=0,
                                   seed=1,
                                   min_count=0,
                                   negative=10,
                                   hs=1)

    # sort by name so the order will be right
    list = sorted(model.wv.index2word)

    # get the score of each node by compering it to all the other nodes
    simple_list = [model.n_similarity(list, [x]) for x in list]

    # print the score of each node
    answer_list = [(x,model.n_similarity(list, [x])) for x in list]
    print(*answer_list, sep="\n")

    return simple_list
