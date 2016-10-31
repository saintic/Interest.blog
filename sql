SELECT a.username, a.email, a.cname, a.avatar, a.motto, a.url, a.time, a.weibo, a.github, a.gender, a.extra FROM User a INNER JOIN OAuth b ON a.username = b.oauth_username;
