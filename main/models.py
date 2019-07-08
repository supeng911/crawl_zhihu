from django.db import models


class Quote(models.Model):
    """
    The scrapped data will be saved in this model
    """
    text = models.TextField()
    author = models.CharField(max_length=512)


class ZhihuArticleModel(models.Model):
    zhihu_id = models.BigIntegerField(primary_key=True)
    author_id = models.CharField("作者ID", max_length=100, null=True)
    title = models.CharField("问题标题", max_length=300, null=True)
    content = models.TextField("问题内容", null=True)
    image_url = models.CharField("封面图片", max_length=300, null=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    crawled_at = models.DateTimeField("爬取得时间", auto_now=True)
    status = models.CharField("对应采集的处理方案", max_length=30, null=True)
    mg_id = models.IntegerField(null=True)
    mg_type = models.CharField("蜜果对应类型", max_length=30, null=True)

    class Meta:
        ordering = ["zhihu_id"]
        db_table = 'crawl_zhihu_article'


class ZhihuCommentModel(models.Model):
    zhihu_id = models.BigIntegerField(primary_key=True)
    author_id = models.CharField("作者ID", max_length=100, null=True)
    content = models.TextField("评论内容", null=True)
    vote_count = models.IntegerField("点赞数量", null=True)
    resource_type = models.CharField("相关内容", max_length=100, null=True)
    resource_id = models.CharField("相关ID", max_length=200, null=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    status = models.CharField("对应采集的处理方案", max_length=30, null=True)
    mg_id = models.IntegerField(null=True)
    crawled_at = models.DateTimeField("爬取得时间", auto_now=True)

    class Meta:
        ordering = ["zhihu_id"]
        db_table = 'crawl_zhihu_comment'


class ZhihuPeopleModel(models.Model):
    zhihu_id = models.CharField("知乎ID", max_length=100, null=True)
    name = models.CharField(max_length=100, null=True)
    url_token = models.CharField(max_length=100, null=True)
    avatar_url = models.CharField(max_length=300, null=True)
    headline = models.CharField(max_length=500, null=True)
    gender = models.IntegerField(null=True)
    mg_id = models.IntegerField(null=True)
    crawled_at = models.DateTimeField("爬取得时间", auto_now=True)

    class Meta:
        ordering = ["zhihu_id"]
        db_table = 'crawl_zhihu_people'


class ZhihuQuestionModel(models.Model):
    zhihu_id = models.BigIntegerField(primary_key=True)
    title = models.CharField("问题标题", max_length=200, null=True)
    content = models.TextField("问题内容", null=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    status = models.CharField("对应采集的处理方案", max_length=30, null=True)
    mg_id = models.IntegerField(null=True)
    crawled_at = models.DateTimeField("爬取得时间", auto_now=True)

    class Meta:
        ordering = ["zhihu_id"]
        db_table = 'crawl_zhihu_question'


class ZhihuAnswerModel(models.Model):
    zhihu_id = models.BigIntegerField(primary_key=True)
    question_id = models.IntegerField("问题ID", null=True)
    author_id = models.CharField("作者ID", max_length=100, null=True)
    content = models.TextField("问题内容", null=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    status = models.CharField("对应采集的处理方案", max_length=30, null=True)
    mg_id = models.IntegerField(null=True)
    crawled_at = models.DateTimeField("爬取得时间", auto_now=True)

    class Meta:
        ordering = ["zhihu_id"]
        db_table = 'crawl_zhihu_answer'
