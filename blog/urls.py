from django.urls import re_path
import blog.index as index
import blog.jury as jury
import blog.message as message
import blog.person_info as person_info
import blog.complaint_detail as complaint_detail
import blog.red_black_list as red_black_list
import blog.search_detail as search_detail
import blog.user as user
import blog.company as company
import blog.tests as tests
import blog.edit_db as edit_db

urlpatterns = [
    # 首页
    re_path(r'^index$', index.index),
    re_path(r'^carousel_map$', index.carousel_map),
    re_path(r'^hot_articles$', index.hot_articles),
    re_path(r'^hot_posts$', index.hot_posts),
    re_path(r'^post_complain$', index.post_complain),
    re_path(r'^latest_posts$', index.latest_posts),
    re_path(r'^write_page$', index.write_page),
    # 评审团
    re_path(r'^jury_page$', jury.jury_page),
    # 消息
    re_path(r'^message$', message.message),
    # 个人主页
    re_path(r'^person_info$', person_info.person_info),
    re_path(r'^person_edit$', person_info.person_edit),
    re_path(r'^person_complain$', person_info.person_complain),
    re_path(r'^person_collection$', person_info.person_collection),
    re_path(r'^person_change$', person_info.person_change),
    re_path(r'^person_reply$', person_info.person_reply),
    # 帖详情
    re_path(r'^post_detail$', complaint_detail.complaint_detail),
    re_path(r'^post_top$', complaint_detail.complaint_top),
    re_path(r'^post_reply$', complaint_detail.complaint_reply),
    re_path(r'^post_comment$', complaint_detail.complaint_comment),
    re_path(r'^complaint_collect$', complaint_detail.complaint_collect),
    re_path(r'^complaint_cancel_collect$', complaint_detail.complaint_cancel_collect),
    # 红黑榜
    re_path(r'^red_black_list$', red_black_list.red_black_list),
    # 搜索详情
    re_path(r'^search_detail$', search_detail.search_detail),
    re_path(r'^search$', search_detail.search),
    # 登录注册
    re_path(r'^login_page$', user.login_page),
    re_path(r'^login$', user.login),
    re_path(r'^register_page$', user.register_page),
    re_path(r'^register$', user.register),
    re_path(r'^logout$', user.logout),
    # 企业相关
    re_path(r'^company_post$', company.company_post),
    re_path(r'^company_post_data$', company.company_post_data),
    # 测试
    re_path(r'^test$', tests.test),
    # 修改
    re_path(r'^edit_page$', edit_db.edit_page),
    re_path(r'^edit_pic$', edit_db.edit_pic),
    re_path(r'^edit_red_black$', edit_db.edit_red_black),
]
