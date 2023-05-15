---
layout: post
title: "[GitBlog] disqus 댓글기능 추가하기" #게시물 이름
tags: [gitblog, disqus, 댓글, 디스커스] #태그 설정
categories: BLOG #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

Github 블로그에 댓글을 추가하기 위한 방법으로는 `disqus`, `utterances`를 이용하면 된다. 
본 글은 `disqus basic 버전`의 적용 과정을 포스팅하며, Jekyll template을 이용해 블로그가 구축되었기 때문에 yaml, html 파일의 내용 구성이 다를 수 있다.


## disqus 설정

### 1. Do something on https://disqus.com/ site

1. <https://disqus.com/>에 접속해 회원가입, 로그인을 하자.   
facebook, twitter, google과 같은 소셜 계정으로 가입이 가능하다. ~~본인은 google로 했다.~~   

<img src="/image/disqus_login.png" alt="disqus_login" style="height: 714px; width:719px;"/>

2. Disqus install 하기   
`I want to install Disqus on my site` 선택   

<img src="/image/disqus_pic1.png" alt="disqus_pic1" style="height: 606px; width:581px;"/>

3. Disqus creat site   
`Website Name`은 unique해야 하며, subdomain으로 활용되기 때문에 기억해두면 된다.   

<img src="/image/disqus_pic2.png" alt="disqus_pic2" style="height: 717px; width:684px;"/>

4. Plan 설정 (요금제)
`plus`,`pro`,`business`,`basic` 중에 역시... basic...   

<img src="/image/disqus_pic3.png" alt="disqus_pic3" style="height: 800px; width:650px;"/>

5. platform 선택   
<img src="/image/disqus_pic4.png" alt="disqus_pic4" style="height: 600px; width:800px;"/>

6. jekyll source code copy



Website Name에 적용할 shortname 작성.
`shortname`.disqus.com이라는 URL을 Jekyll config 파일에 작성해야함.
  <aside>
  💡 priority, changefreq와 같은 값은 포털사이트의 검색엔진 설정에 따라 무시가 될 수 있다.
  </aside>  


sitemap.xml을 자동으로 갱신하기 위한 코드는 다음 [sitemap.xml][sitemap]파일을 활용하면 된다.
~~코드 자체를 올리고 싶었으나, 웹페이지에서 자동으로 변환되어 보여지기 때문에 github 링크로 대체 합니다.~~


<img src="/image/sitemap_xml.png" alt="sitemap" style="height: 500px; width:950px;"/>

위 사진에서 보이는 것 처럼, 블로그의 모든 글의 URL이 등록되어 있다. sitemap.xml을 검색엔진에 제출한다고 해서 모든 제출된 웹페이지(URL)을 색인해준다는 보장이 없다. 또한, 검색엔진이 웹 페이지를 크롤링하여 URL을 발견하는 메커니즘을 보완하기 위한 파일이지, 그 기능을 전부 대체하는 파일은 아니다.


### robots.txt 생성하기

robots.txt는 검색엔진의 크롤러가 웹(자신의 Gitblog)에 접근할 때 지켜야하는 규칙과 정보를 명시하기 위한 파일이다. 디렉토리 구조인 GitHub Blog에서 `특정 디렉토리(일기, 다이어리, etc), 컨텐츠`를 크롤링하지 않도록 규칙을 명시하는 것이다.


다음과 같은 컨텐츠의 크롤링을 금지하기 위해 robots.txt를 활용한다.
- 개인 정보 페이지
- 사이트 관리자를 위한 컨텐츠
- 이미지파일 or 기타 파일
- +@ 사이트를 리뉴얼할 때 임시적으로 컨텐츠를 검색되지 않도록.


robots.txt
```
User-agent: *
Allow: /
Disallow: /scripts
Sitemap: https://byj1009.github.io/sitemap.xml
```



---
### Reference
- [https://www.ascentkorea.com/][ascentkorea]
- [https://yenarue.github.io/tip/2020/04/30/Search-SEO/][yenarue]

[sitemap]: https://github.com/byj1009/byj1009.github.io/blob/4fa8af2025abf18de07c8094607b8c00ba1ae592/sitemap.xml
