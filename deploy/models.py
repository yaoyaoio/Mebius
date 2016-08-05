from django.db import models

# Create your models here.

#定义salt表
class SaltMinion(models.Model):
    name = models.CharField('Minion名称',max_length=124)
    create_date = models.DateField('创建时间',auto_now_add=True)
    status_choices = (
        (1, u'已经认证'),
        (2, u'未认证'),
    )
    status = models.SmallIntegerField('认证状态',choices=status_choices)
    Autherized_date = models.DateField('认证时间',auto_now=True)
    memo = models.TextField(u'备注', null=True,blank=True)
    def ___str__(self):
        return self.name
    class Meta:
        verbose_name = 'Salt认证'
        verbose_name_plural = 'Salt认证'
    def colored_status(self):
        if self.status == 1:
            cell_html = '<span style="background: orange;">%s</span>'
        elif self.status == 2 :
            cell_html = '<span style="background: yellowgreen;">%s</span>'
        else:
            cell_html = '<span >%s</span>'
        return cell_html % self.get_status_display()
    colored_status.allow_tags = True
    colored_status.short_description = u'认证状态'