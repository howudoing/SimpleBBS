#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/24 19:30
# @Author  : Wayne Li

def add_node(tree_dic, comment):
    if comment.parent_comment is None:
        # 如果没有parent，则本身即为parent
        tree_dic[comment] = {}
    else:
        for k, v in tree_dic.items():
            if k == comment.parent_comment:
                # 找到父节点
                tree_dic[k][comment] = {}
            else:
                add_node(v, comment)


def render_tree_node(tree_dic, margen_value):
    html = ""
    for k, v in tree_dic.items():
        ele = "<div class='comment-node' style='margin-left: %spx'>" % margen_value + k.comment + \
              "<span style='margin-left: 20px'>%s</span>" % k.date \
              + "<span style='margin-left: 20px'>%s</span>" % k.user.name \
              + '<span comment-id="%s"' % k.id + ' class="glyphicon glyphicon-comment pull-right add-comment" aria-hidden="true"></span>' + "</div>"
        html += ele
        html += render_tree_node(v, margen_value + 20)
    return html


def render_comment_tree(tree_dic):
    html = ""
    for k, v in tree_dic.items():
        ele = "<div class='root-comment'>" + k.comment + "<span style='margin-left: 20px'>%s</span>" % k.date \
              + "<span style='margin-left: 20px'>%s</span>" % k.user.name \
              + '<span comment-id="%s"' % k.id + ' class="glyphicon glyphicon-comment pull-right add-comment" aria-hidden="true"></span>' + "</div>"
        html += ele
        html += render_tree_node(v, 20)
    return html


def build_tree(comment_set):
    # print(comment_set)
    tree_dic = {}
    for comment in comment_set:
        add_node(tree_dic, comment)
    return tree_dic
