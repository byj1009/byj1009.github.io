---
layout: post
title: "[GitBlog] 검색엔진에 등록하기" #게시물 이름
tags: [gitblog, google, naver, 검색엔진, blog] #태그 설정
categories: Github blog #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

GitHub 블로그를 개설한 이후로 포스팅이 점점 귀찮아지는 것 같아, 절치부심하기 위해 검색엔진에 등록을 하기로 결심했다.

우리가 포탈사이트를 통해 특정 단어 및 주제의 자료를 찾고자 할 때, 포탈사이트 검색엔진의 크롤러는 웹페이지의 콘텐츠들을 찾아 주제별로 색인(index)하고, 검색어와 일치하는 색인(Index)의 결과만을 노출하게 된다. 

> 즉, 구글과 네이버에서 주기적으로 인터넷상에 올라온 컨텐츠들을 크롤링(수집)해 주제별로 색인(index)하며, 사용자가 검색시 index값이 일치하는 자료를 노출하는 것이다.

마케팅을 위해 검색엔진에 최대한 노출이 많이 되기 위한 작업으로 `SEO(Search Engine Optimization) 검색 엔진 최적화` 를 수행한다. 하지만... 본 블로그가 ~~아직은(?)~~ SEO까지 신경쓸 만한 단계는 아니므로, 등록했던 절차에 대해서만 포스팅하도록 한다.

사이트에 방문하는 검색엔진의 크롤러를 제어하기 위한 설정 파일인 `로봇 텍스트 파일(robots.txt)` & `사이트맵 파일(sitemap.xml)` 을 생성해보고, 포털사이트의 검색엔진에 GitHub Blog를 등록을 해보자.


## 검색엔진 크롤러 제어 파일(sitemap.xml, robots.txt) 생성

### sitemap.xml 생성하기
sitemap.xml은 사이트에 방문하는 검색엔진의 크롤러에게 컨텐츠를(내가 포스팅한 글) 제공하기 위해 URL 모두를 XML 파일 형식으로 작성한 것이다. 새로운 글이 작성될 때마다, sitemap.xml에 해당 URL을 업데이트 해야하지만, 이 또한 자동화가 가능하다.

   
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
[https://www.ascentkorea.com/][ascentkorea]
[https://yenarue.github.io/tip/2020/04/30/Search-SEO/][yenarue]

[sitemap]: https://github.com/byj1009/byj1009.github.io/blob/4fa8af2025abf18de07c8094607b8c00ba1ae592/sitemap.xml
[ascentkorea]: https://www.ascentkorea.com/what-is-robots-txt-sitemap-xml/
[yenarue]: https://yenarue.github.io/tip/2020/04/30/Search-SEO/