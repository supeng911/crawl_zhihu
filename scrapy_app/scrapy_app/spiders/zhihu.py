# -*- coding: utf-8 -*-
import scrapy
import json
import logging
import time


def timestamp_to_str(timestamp):
    timeArray = time.localtime(timestamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

    return otherStyleTime


class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ['zhihu.com']

    topics = [
        19550917
    ]

    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhihu.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    feed_list_start_url = "https://www.zhihu.com/api/v4/topics/{0}/feeds/top_activity?include=data%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Dpeople%29%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Darticle%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dquestion%29%5D.target.annotation_detail%2Ccomment_count%3B&limit=5&after_id=0"

    answer_list_url = "https://www.zhihu.com/api/v4/questions/{0}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset={1}&sort_by=default"

    people_info_url = "https://www.zhihu.com/api/v4/members/{0}"

    answer_comments_list_url = "https://www.zhihu.com/api/v4/answers/{0}/root_comments?include=data%5B*%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author&order=normal&limit=20&offset=0&status=open"

    article_comments_list_url = "https://www.zhihu.com/api/v4/articles/{0}/root_comments?include=data%5B*%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author&order=normal&limit=20&offset=0&status=open"

    def start_requests(self):
        for topic_id in self.topics:
            yield scrapy.Request(url=self.feed_list_start_url.format(topic_id),
                                 headers=self.headers,
                                 callback=self.parse_feed_list)

    def parse_feed_list(self, response):
        """
        处理 topic 的 feed list
        :param response:
        :return:
        """
        feed_json = json.loads(response.text)
        is_end = feed_json["paging"]["is_end"]
        next_url = feed_json["paging"]["next"]

        for feed_item in feed_json["data"]:
            item_type = feed_item["target"]["type"]

            if item_type == "article":
                logging.warning("+++++++++++ 开始处理文章ID：%s", str(feed_item["target"]["id"]))
                author_id = feed_item["target"]["author"]["id"] if "id" in feed_item["target"]["author"] else None
                image_url = feed_item["target"]["image_url"] if "image_url" in feed_item["target"] else None

                yield {
                    "type": "article",
                    "zhihu_id": feed_item["target"]["id"],
                    "author_id": author_id,
                    "title": feed_item["target"]["title"],
                    "content": feed_item["target"]["content"],
                    "image_url": image_url,
                    "created_at": timestamp_to_str(feed_item["target"]["created"]),
                    "updated_at": timestamp_to_str(feed_item["target"]["updated"])
                }
                # 采集评论信息
                yield scrapy.Request(url=self.article_comments_list_url.format(feed_item["target"]["id"]),
                                     headers=self.headers,
                                     meta={"resource_type": "article", "resource_id": feed_item["target"]["id"]},
                                     callback=self.parse_comment)

                if not author_id is None:
                    # 采集用户信息
                    yield scrapy.Request(url=self.people_info_url.format(author_id),
                                         headers=self.headers,
                                         callback=self.parse_people)
            elif item_type == "answer":
                question_id = feed_item["target"]["question"]["id"]
                created_time = feed_item["target"]["question"]["created"]
                question_url = "https://www.zhihu.com/question/" + str(question_id)

                yield scrapy.Request(url=question_url,
                                     headers=self.headers,
                                     meta={"question_id": question_id, "created_time": created_time},
                                     callback=self.parse_question)
            else:
                logging.warning("没有处理的 type: %s ==== json is: %s", item_type, json.dumps(feed_item))

        # 处理下一页请求
        if not is_end:
            yield scrapy.Request(url=next_url,
                                 headers=self.headers,
                                 callback=self.parse_feed_list)

    def parse_comment(self, response):
        """
        处理 评论信息
        :param response:
        :return:
        """
        logging.warning("---- 采集评论", )
        resource_type = response.meta.get("resource_type", "")
        resource_id = response.meta.get("resource_id", "")

        re_json = json.loads(response.text)
        is_end = re_json["paging"]["is_end"]
        next_url = re_json["paging"]["next"]

        # 提取reply的具体字段
        for reply in re_json["data"]:
            author_id = reply["author"]["member"]["id"] if "id" in reply["author"]["member"] else None

            yield {
                "type": "comment",
                "zhihu_id": reply["id"],
                "author_id": author_id,
                "content": reply["content"],
                "resource_type": resource_type,
                "resource_id": resource_id,
                "created_at": timestamp_to_str(reply["created_time"]),
                "updated_at": timestamp_to_str(reply["created_time"]),
                "vote_count": reply["vote_count"],
            }

            # 采集 用户信息
            if not author_id is None:
                yield scrapy.Request(url=self.people_info_url.format(author_id),
                                     headers=self.headers,
                                     callback=self.parse_people)

        if not is_end:
            # 采集下一页
            yield scrapy.Request(url=next_url,
                                 headers=self.headers,
                                 meta={"resource_type": resource_type, "resource_id": resource_id},
                                 callback=self.parse_comment)

    def parse_people(self, response):
        logging.warning("---- 采集用户", )
        user_json = json.loads(response.text)

        if user_json:
            yield {
                "type": "people",
                "zhihu_id": user_json["id"],
                "name": user_json["name"],
                "url_token": user_json["url_token"],
                "avatar_url": user_json["avatar_url_template"].replace("{size}", "hd"),
                "headline": user_json["headline"],
                "gender": user_json["gender"],
            }

    def parse_question(self, response):
        """
        采集知乎的问题
        :param response:
        :return:
        """
        question_id = response.meta.get("question_id", "")
        logging.warning("+++++++++++ 开始处理问题ID：%s", str(question_id))
        created_time = response.meta.get("created_time", "")
        title = response.css("h1.QuestionHeader-title::text").extract()[0]
        content = None
        try:
            content = response.css("div.QuestionHeader-detail span.RichText.ztext::text").extract()[0]
        except:
            content = None
        # topics = response.css(".QuestionHeader-topics .Popover div::text").extract()

        yield {
            "type": "question",
            "zhihu_id": question_id,
            "title": title,
            "content": content,
            "created_at": timestamp_to_str(created_time),
            "updated_at": timestamp_to_str(created_time)
        }

        answers_url = self.answer_list_url.format(question_id, 0)

        yield scrapy.Request(url=answers_url,
                             headers=self.headers,
                             meta={"question_id": question_id},
                             callback=self.parse_answers)

    def parse_answers(self, response):
        """
        采集知乎的回答
        :param response:
        :return:
        """
        question_id = response.meta.get("question_id", "")

        # 处理question的answer
        ans_json = json.loads(response.text)
        is_end = ans_json["paging"]["is_end"]
        next_url = ans_json["paging"]["next"]

        for answer in ans_json["data"]:
            logging.warning("---- 采集回答", )
            author_id = answer["author"]["id"] if "id" in answer["author"] else None

            yield {
                "type": "answer",
                "zhihu_id": answer["id"],
                "question_id": question_id,
                "author_id": author_id,
                "content": answer["content"] if "content" in answer else None,
                "created_at": timestamp_to_str(answer["created_time"]),
                "updated_at": timestamp_to_str(answer["updated_time"])
            }

            # 采集评论信息
            yield scrapy.Request(url=self.answer_comments_list_url.format(answer["id"]),
                                 headers=self.headers,
                                 meta={"resource_type": "answer", "resource_id": answer["id"]},
                                 callback=self.parse_comment)

            if not author_id is None:
                # 采集用户信息
                yield scrapy.Request(url=self.people_info_url.format(author_id),
                                     headers=self.headers,
                                     callback=self.parse_people)

        if not is_end:
            yield scrapy.Request(url=next_url,
                                 headers=self.headers,
                                 meta={"question_id": question_id},
                                 callback=self.parse_answers)
