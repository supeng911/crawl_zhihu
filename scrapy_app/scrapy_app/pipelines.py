# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from main.models import Quote, ZhihuArticleModel, ZhihuCommentModel, ZhihuPeopleModel, ZhihuQuestionModel, \
    ZhihuAnswerModel


class ScrapyAppPipeline(object):
    def process_item(self, item, spider):
        if item.get("type") == "article":
            article = ZhihuArticleModel(zhihu_id=int(item.get("zhihu_id")),
                                        author_id=item.get("author_id"),
                                        title=item.get("title"),
                                        content=item.get("content"),
                                        image_url=item.get("image_url"),
                                        created_at=item.get("created_at"),
                                        updated_at=item.get("updated_at"))
            article.save()
        elif item.get("type") == "comment":
            comment = ZhihuCommentModel(zhihu_id=int(item.get("zhihu_id")),
                                        author_id=item.get("author_id"),
                                        content=item.get("content"),
                                        vote_count=item.get("vote_count"),
                                        resource_type=item.get("resource_type"),
                                        resource_id=item.get("resource_id"),
                                        created_at=item.get("created_at"),
                                        updated_at=item.get("updated_at"))
            comment.save()
        elif item.get("type") == "people":
            people = ZhihuPeopleModel(zhihu_id=item.get("zhihu_id"),
                                      name=item.get("name"),
                                      url_token=item.get("url_token"),
                                      avatar_url=item.get("avatar_url"),
                                      headline=item.get("headline"),
                                      gender=item.get("gender"))
            people.save()
        elif item.get("type") == "question":
            question = ZhihuQuestionModel(zhihu_id=int(item.get("zhihu_id")),
                                          title=item.get("title"),
                                          content=item.get("content"),
                                          created_at=item.get("created_at"),
                                          updated_at=item.get("updated_at"))
            question.save()
        elif item.get("type") == "answer":
            answer = ZhihuAnswerModel(zhihu_id=int(item.get("zhihu_id")),
                                      question_id=item.get("question_id"),
                                      author_id=item.get("author_id"),
                                      content=item.get("content"),
                                      created_at=item.get("created_at"),
                                      updated_at=item.get("updated_at"))
            answer.save()
        return item
