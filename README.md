## Everblog
	——使用evernote作为blog的后台db

As you know，Evernote是目前最优秀的笔记应用，它包括标签(tag)、笔记本(notebook)、笔记(note)等元素，提供分享、协同编辑、查找等功能，免费帐户每月60M的上传基本上可以满足普通用户的需求。

另外仍有很多爱好写博客的朋友，经常在主机、空间、域名这些事情上费时费力。

那么没有一种方式，可以将Evernote作为blog的数据存储db呢？这样就可以省去大量的时间，专注于内容创作了。想到这一点，于是我想到了Everblog...

我想做这样一件事情，使用Evernote的客户端、网页版等进行内容编辑，使用Evernote的存储功能作为db，将特定的内容(可配置)集中展示在一个domain下，写作、更新在Evernote中进行，前端作为一个Blog式样，仅进行展示，集note和blog与一体。


#### BTW

+ Evernote可以分享笔记、笔记本，但是是“零碎”的，一方面不能集中展示，另一方面我想加入可配的条件，仅展示“特定内容”(Todo)

+ Evernote现在的问题是连接响应太慢，作为db会影响体验(一个简单的想法是吧tag和note相关的id放入内存中)
//补充,考虑使用Redis

+ 目前仅完成基本查询功能，Todo很多 

#### Tech

+ 使用了Evernote[官方的python库](https://github.com/evernote/evernote-sdk-python)与Evernote交互

+ 使用了Python的flask+jinja2

[@nourlcn](https://twitter.com/nourlcn)


