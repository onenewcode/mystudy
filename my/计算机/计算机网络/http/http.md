# 了解 Web 及网络基础
## 诞生
**WWW构建技术**
现在已提出了 3 项 WWW 构建技术，分别是：把 SGML（Standard Generalized Markup Language，标准通用标记语言）作为页面的文本标记语言的 HTML（HyperText Markup Language，超文本标记语言）；作为文档传递协议的 HTTP ；指定文档所在地址的 URL（Uniform Resource Locator，统一资源定位符）。
## 网络基础 TCP/IP
通常使用的网络（包括互联网）是在 TCP/IP 协议族的基础上运作的。而 HTTP 属于它内部的一个子集。

### TCP/IP 协议族
计算机与网络设备要相互通信，双方就必须基于相同的方法。比如，如何探测到通信目标、由哪一边先发起通信、使用哪种语言进行通信、怎样结束通信等规则都需要事先确定。不同的硬件、操作系统之间的通信，所有的这一切都需要一种规则。而我们就把这种规则称为协议（protocol）。
<img src="img/屏幕截图 2022-12-02 183816.png">

协议中存在各式各样的内容。从电缆的规格到 IP 地址的选定方法、寻找异地用户的方法、双方建立通信顺序，以及 Web 页面显示需要处理的步骤，等等。
像这样把与互联网相关联的协议集合起来总称为 TCP/IP。也有说法认为，TCP/IP 是指 TCP 和 IP 这两种协议。还有一种说法认为，TCP/ IP 是在 IP 协议的通信过程中，使用到的协议族的统称。
### TCP/IP 的分层管理
TCP/IP 协议族里重要的一点就是分层。TCP/IP 协议族按层次分别分为以下 4 层：应用层、传输层、网络层和数据链路层。
TCP/IP 协议族各层的作用如下。
**应用层**
应用层决定了向用户提供应用服务时通信的活动。
TCP/IP 协议族内预存了各类通用的应用服务。比如，FTP（File Transfer Protocol，文件传输协议）和DNS（Domain Name System，域名系统）服务就是其中两类。
HTTP 协议也处于该层。
**传输层**
传输层对上层应用层，提供处于网络连接中的两台计算机之间的数据传输。
在传输层有两个性质不同的协议：TCP（Transmission Control Protocol，传输控制协议）和 UDP（UserData Protocol，用户数据报协议）。
**网络层（又名网络互连层）**
网络层用来处理在网络上流动的数据包。数据包是网络传输的最小数据单位。该层规定了通过怎样的路径（所谓的传输路线）到达对方计算机，并把数据包传送给对方。
与对方计算机之间通过多台计算机或网络设备进行传输时，网络层所起的作用就是在众多的选项内选择一条传输路线。
**链路层（又名数据链路层，网络接口层）**
用来处理连接网络的硬件部分。包括控制操作系统、硬件的设备驱动、NIC（Network Interface Card，网络适配器，即网卡），及光纤等物理可见部分（还包括连接器等一切传输媒介）。硬件上的范畴均在链路层的作用范围之内。
### TCP/IP 通信传输流
<img src="img\屏幕截图 2022-12-02 193438.png">

### 与 HTTP 关系密切的协议 : IP、TCP 和 DNS
下面我们分别针对在 TCP/IP 协议族中与 HTTP 密不可分的 3 个协议（IP、TCP 和 DNS）进行说明。
#### 负责传输的 IP 协议
按层次分，IP（Internet Protocol）网际协议位于网络层。Internet Protocol 这个名称可能听起来有点夸张，但事实正是如此，因为几乎所有使用网络的系统都会用到 IP 协议。TCP/IP 协议族中的 IP 指的就是网际协议。IP 协议的作用是把各种数据包传送给对方。而要保证确实传送到对方那里，则需要满足各类条件。其中两个重要的条件是 IP 地址和 MAC 地址（Media Access Control Address）。IP 地址指明了节点被分配到的地址，MAC 地址是指网卡所属的固定地址。
**使用 ARP 协议凭借 MAC 地址进行通信**
IP 间的通信依赖 MAC 地址。在网络上，通信的双方在同一局域网（LAN）内的情况是很少的，通常是经过多台计算机和网络设备中转才能连接到对方。而在进行中转时，会利用下一站中转设备的 MAC 地址来搜索下一个中转目标。这时，会采用 ARP 协议（Address Resolution Protocol）。ARP 是一种用以解析地址的协议，根据通信方的 IP 地址就可以反查出对应的 MAC 地址。没有人能够全面掌握互联网中的传输状况在到达通信目标前的中转过程中，那些计算机和路由器等网络设备只能获悉很粗略的传输路线。这种机制称为路由选择（routing），
<img src="\img\屏幕截图 2022-12-05 081202.png">

####  确保可靠性的 TCP 协议
按层次分，TCP 位于传输层，提供可靠的字节流服务。所谓的字节流服务（Byte Stream Service）是指，为了方便传输，将大块数据分割成以报文段（segment）为单位的数据包进行管理。

为了准确无误地将数据送达目标处，TCP 协议采用了三次握手（three-way handshaking）策略。用 TCP协议把数据包送出去后，TCP 不会对传送后的情况置之不理，它一定会向对方确认是否成功送达。握手过程中使用了 TCP 的标志（flag） —— SYN（synchronize） 和 ACK（acknowledgement）。发送端首先发送一个带 SYN 标志的数据包给对方。接收端收到后，回传一个带有 SYN/ACK 标志的数据包以示传达确认信息。最后，发送端再回传一个带 ACK 标志的数据包，代表“握手”结束。若在握手过程中某个阶段莫名中断，TCP 协议会再次以相同的顺序发送相同的数据包。
<img src="img\屏幕截图 2022-12-05 081514.png">

###### 负责域名解析的 DNS 服务
DNS（Domain Name System）服务是和 HTTP 协议一样位于应用层的协议。它提供域名到 IP 地址之间的解析服务。
计算机既可以被赋予 IP 地址，也可以被赋予主机名和域名。比如 www.hackr.jp。
用户通常使用主机名或域名来访问对方的计算机，而不是直接通过 IP 地址访问。因为与 IP 地址的一组为了解决上述的问题，DNS 服务应运而生。DNS 协议提供通过域名查找 IP 地址，或逆向从 IP 地址反查域名的服务。
<img src="img\屏幕截图 2022-12-05 081834.png">

## 各种协议与 HTTP 协议的关系
学习了和 HTTP 协议密不可分的 TCP/IP 协议族中的各种协议后，我们再通过这张图来了解下 IP 协议、TCP 协议和 DNS 服务在使用 HTTP 协议的通信过程中各自发挥了哪些作用
<img src="img\屏幕截图 2022-12-05 081956.png">

# 简单的 HTTP 协议
##  通过请求和响应的交换达成通信
HTTP 协议规定，请求从客户端发出，最后服务器端响应该请求并返回。换句话说，肯定是先从客户端开始建立通信的，服务器端在没有接收到请求之前不会发送响应。
下面，我们来看一个具体的示例。
<img src="img\屏幕截图 2022-12-05 082827.png">

<img src="img\屏幕截图 2022-12-05 083019.png">

## HTTP 是不保存状态的协议
HTTP 是一种不保存状态，即无状态（stateless）协议。HTTP 协议自身不对请求和响应之间的通信状态进行保存。也就是说在 HTTP 这个级别，协议对于发送过的请求或响应都不做持久化处理。
使用 HTTP 协议，每当有新的请求发送时，就会有对应的新响应产生。协议本身并不保留之前一切的请求或响应报文的信息。这是为了更快地处理大量事务，确保协议的可伸缩性，而特意把 HTTP 协议设计成如
此简单的。

## 告知服务器意图的 HTTP 方法
**GET ：**获取资源
**POST：**传输实体主体
**PUT：**传输文件
PUT 方法用来传输文件。就像 FTP 协议的文件上传一样，要求在请求报文的主体中包含文件内容，然后保存到请求 URI 指定的位置。但是，鉴于 HTTP/1.1 的 PUT 方法自身不带验证机制，任何人都可以上传文件 , 存在安全性问题，因此一般的 Web 网站不使用该方法。若配合 Web 应用程序的验证机制，或架构设计采用REST（REpresentational State Transfer，表征状态转移）标准的同类 Web 网站，就可能会开放使用
**HEAD：**获得报文首部
**DELETE：**删除文件
**OPTIONS：**询问支持的方法
**TRACE：**追踪路径
TRACE 方法是让 Web 服务器端将之前的请求通信环回给客户端的方法。

**CONNECT：**要求用隧道协议连接代理
CONNECT 方法要求在与代理服务器通信时建立隧道，实现用隧道协议进行 TCP 通信。主要使用SSL（Secure Sockets Layer，安全套接层）和 TLS（Transport Layer Security，传输层安全）协议把通信内容加 密后经网络隧道传输。

## 持久连接节省通信量
### 持久连接
HTTP/1.1 和一部分的 HTTP/1.0 想出了持久连接（HTTP PersistentConnections，也称为 HTTP keep-alive 或 HTTP connection reuse）的方法。持久连接的特点是，只要任意一端没有明确提出断开连接，则保持 TCP 连接状态。
### 管线化
持久连接使得多数请求以管线化（pipelining）方式发送成为可能。从前发送请求后需等待并收到响应，才能发送下一个请求。管线化技术出现后，不用等待响应亦可直接发送下一个请求。
## 使用 Cookie 的状态管理
Cookie 技术。Cookie 技术通过在请求和响应报文中写入 Cookie 信息来控制客户端的状态。Cookie 会根据从服务器端发送的响应报文内的一个叫做 Set-Cookie 的首部字段信息，通知客户端保存Cookie。当下次客户端再往该服务器发送请求时，客户端会自动在请求报文中加入 Cookie 值后发送出去。
服务器端发现客户端发送过来的 Cookie 后，会去检查究竟是从哪一个客户端发来的连接请求，然后对比服务器上的记录，最后得到之前的状态信息。
#  HTTP 报文内的 HTTP 信息
## 请求报文及响应报文的结构
<img src="img\屏幕截图 2022-12-05 085135.png">

<img src="img\屏幕截图 2022-12-05 085209.png">

**请求行**
包含用于请求的方法，请求 URI 和 HTTP 版本。
**状态行**
包含表明响应结果的状态码，原因短语和 HTTP 版本。
**首部字段**
包含表示请求和响应的各种条件和属性的各类首部。
一般有 4 种首部，分别是：通用首部、请求首部、响应首部和实体首部。
**其他**
可能包含 HTTP 的 RFC 里未定义的首部（Cookie 等）。
## 编码提升传输速率
HTTP 在传输数据时可以按照数据原貌直接传输，但也可以在传输过程中通过编码提升传输速率。通过在传输时编码，能有效地处理大量的访问请求。但是，编码的操作需要计算机来完成，因此会消耗更多的CPU 等资源。
### 压缩传输的内容编码
向待发送邮件内增加附件时，为了使邮件容量变小，我们会先用 ZIP 压缩文件之后再添加附件发送。HTTP 协议中有一种被称为内容编码的功能也能进行类似的操作。内容编码指明应用在实体内容上的编码格式，并保持实体信息原样压缩。内容编码后的实体由客户端接收并负责解码。
图：内容编码
常用的内容编码有以下几种。
gzip（GNU zip）
compress（UNIX 系统的标准压缩）
deflate（zlib）
identity（不进行编码）
### 分割发送的分块传输编码
在 HTTP 通信过程中，请求的编码实体资源尚未全部传输完成之前，浏览器无法显示请求页面。在传输大容量数据时，通过把数据分割成多块，能够让浏览器逐步显示页面。这种把实体主体分块的功能称为分块传输编码（Chunked Transfer Coding）。

分块传输编码会将实体主体分成多个部分（块）。每一块都会用十六进制来标记块的大小，而实体主体的最后一块会使用“0(CR+LF)”来标记。
HTTP/1.1 中存在一种称为传输编码（Transfer Coding）的机制，它可以在通信时按某种编码方式传输，但只定义作用于分块传输编码中。
## 发送多种数据的多部分对象集合
发送邮件时，我们可以在邮件里写入文字并添加多份附件。这是因为采用了 MIME（MultipurposeInternet Mail Extensions，多用途因特网邮件扩展）机制，它允许邮件处理文本、图片、视频等多个不同类型的数据。例如，图片等二进制数据以 ASCII 码字符串编码的方式指明，就是利用 MIME 来描述标记数据类型。而在 MIME 扩展中会使用一种称为多部分对象集合（Multipart）的方法，来容纳多份不同类型的数据。
相应地，HTTP 协议中也采纳了多部分对象集合，发送的一份报文主体内可含有多类型实体。通常是在图片或文本文件等上传时使用。
多部分对象集合包含的对象如下。
multipart/form-data
在 Web 表单文件上传时使用。
multipart/byteranges
状态码 206（Partial Content，部分内容）响应报文包含了多个范围的内容时使用。
multipart/form-data
```s
Content-Type: multipart/form-data; boundary=AaB03x
--AaB03x
Content-Disposition: form-data; name="field1"
Joe Blow
--AaB03x
Content-Disposition: form-data; name="pics"; filename="file1.txt"
Content-Type: text/plain
...（file1.txt的数据）...
--AaB03x--
```
multipart/byteranges
```s
HTTP/1.1 206 Partial Content
Date: Fri, 13 Jul 2012 02:45:26 GMT
Last-Modified: Fri, 31 Aug 2007 02:02:20 GMT
Content-Type: multipart/byteranges; boundary=THIS_STRING_SEPARATES
--THIS_STRING_SEPARATES
Content-Type: application/pdf
Content-Range: bytes 500-999/8000
...（范围指定的数据）...
--THIS_STRING_SEPARATES
Content-Type: application/pdf
Content-Range: bytes 7000-7999/8000
...（范围指定的数据）...
--THIS_STRING_SEPARATES--
```
在 HTTP 报文中使用多部分对象集合时，需要在首部字段里加上 Content-type。使用 boundary 字符串来划分多部分对象集合指明的各类实体。在 boundary 字符串指定的各个实体的起始行之前插入“--”标记（例如：--AaB03x、--THIS_STRING_SEPARATES），而在多部分对象集合对应的字符串的最后插入“--”标记（例如：--AaB03x--、--THIS_STRING_SEPARATES--）作为结尾.
## 获取部分内容的范围请求
如果下载过程中遇到网络中断的情况，那就必须重头开始。为了解决上述问题，需要一种可恢复的机制。所谓恢复是指能从之前下载中断处恢复下载。
<img src="img\image.png">

## 内容协商返回最合适的内容
内容协商机制是指客户端和服务器端就响应的资源内容进行交涉，然后提供给客户端最为适合的资源。内容协商会以响应资源的语言、字符集、编码方式等作为判断的基准。
包含在请求报文中的某些首部字段（如下）就是判断的基准。这些首部字
Accept
Accept-Charset
Accept-Encoding
Accept-Language
Content-Language
内容协商技术有以下 3 种类型。
**服务器驱动协商（Server-driven Negotiation）**
由服务器端进行内容协商。以请求的首部字段为参考，在服务器端自动处理。但对用户来说，以浏览器发送的信息作为判定的依据，并不一定能筛选出最优内容。
**客户端驱动协商（Agent-driven Negotiation）**
由客户端进行内容协商的方式。用户从浏览器显示的可选项列表中手动选择。还可以利用 JavaScript 脚本在 Web 页面上自动进行上述选择。
**透明协商（Transparent Negotiation）**
是服务器驱动和客户端驱动的结合体，是由服务器端和客户端各自进行内容协商的一种方法。

# 返回结果的 HTTP 状态码
HTTP 状态码负责表示客户端 HTTP 请求的返回结果、标记服务器端的处理是否正常、通知出现的错误等工作

##  2XX 成功
2XX 的响应结果表明请求被正常处理了。
**200 OK**
表示从客户端发来的请求在服务器端被正常处理了。
**204 No Content**
该状态码代表服务器接收的请求已成功处理，但在返回的响应报文中不含实体的主体部分。另外，也不允许返回任何实体的主体。比如，当从浏览器发出请求处理后，返回 204 响应，那么浏览器显示的页面不发生更新。一般在只需要从客户端往服务器发送信息，而对客户端不需要发送新信息内容的情况下使用。
**206 Partial Content**
该状态码表示客户端进行了范围请求，而服务器成功执行了这部分的 GET 请求。响应报文中包含由Content-Range 指定范围的实体内容
## 3XX 重定向
3XX 响应结果表明浏览器需要执行某些特殊的处理以正确处理请求。
**301 Moved Permanently**
永久性重定向。该状态码表示请求的资源已被分配了新的 URI，以后应使用资源现在所指的 URI。也就是说，如果已经把资源对应的 URI 保存为书签了，这时应该按 Location 首部字段提示的 URI 重新保存。
http://example.com/sample
**302 Found**
临时性重定向。该状态码表示请求的资源已被分配了新的 URI，希望用户（本次）能使用新的 URI 访问。
**303 See Other**
该状态码表示由于请求对应的资源存在着另一个 URI，应使用 GET 方法定向获取请求的资源。
303 状态码和 302 Found 状态码有着相同的功能，但 303 状态码明确表示客户端应当采用 GET 方法获取资源.
**304 Not Modified**
该状态码表示客户端发送附带条件的请求时，服务器端允许请求访问资源，但未满足条件的情况。304状态码返回时，不包含任何响应的主体部分。
**307 Temporary Redirect**
临时重定向。该状态码与 302 Found 有着相同的含义。尽管 302 标准禁止 POST 变换成 GET，但实际使用时大家并不遵守。
307 会遵照浏览器标准，不会从 POST 变成 GET。但是，对于处理响应时的行为，每种浏览器有可能出现不同的情况。

## 4XX 客户端错误
4XX 的响应结果表明客户端是发生错误的原因所在。
**400 Bad Request**
该状态码表示请求报文中存在语法错误。当错误发生时，需修改请求的内容后再次发送请求。另外，浏览器会像 200 OK 一样对待该状态码。
**401 Unauthorized**
该状态码表示发送的请求需要有通过 HTTP 认证（BASIC 认证、DIGEST 认证）的认证信息。另外若之前已进行过 1 次请求，则表示用 户认证失败。返回含有 401 的响应必须包含一个适用于被请求资源的 WWW-Authenticate 首部用以质询（challenge）
用户信息。当浏览器初次接收到 401 响应，会弹出认证用的对话窗口。
**403 Forbidden**
该状态码表明对请求资源的访问被服务器拒绝了。服务器端没有必要给出拒绝的详细理由，但如果想作说明的话，可以在实体的主体部分对原因进行描述，这样就能让用户看到了。未获得文件系统的访问授权，访问权限出现某些问题（从未授权的发送源 IP 地址试图访问）等列举的情
况都可能是发生 403 的原因。
**404 Not Found**
该状态码表明服务器上无法找到请求的资源。除此之外，也可以在服务器端拒绝请求且不想说明理由时使用。
## 5XX 服务器错误
5XX 的响应结果表明服务器本身发生错误。
**500 Internal Server Error**
该状态码表明服务器端在执行请求时发生了错误。也有可能是 Web 应用存在的 bug 或某些临时的故障。
**503 Service Unavailable**
该状态码表明服务器暂时处于超负载或正在进行停机维护，现在无法处理请求。如果事先得知解除以上状况需要的时间，最好写入 RetryAfter 首部字段再返回给客户端。

# 与 HTTP 协作的 Web 服务器
一台 Web 服务器可搭建多个独立域名的 Web 网站，也可作为通信路径上的中转服务器提升传输效率。
## 用单台虚拟主机实现多个域名
即使物理层面只有一台服务器，但只要使用虚拟主机的功能，则可以假想已具有多台服务器
<img src="img\屏幕截图 2022-12-05 093227.png">

## 通信数据转发程序 ：代理、网关、隧道
HTTP 通信时，除客户端和服务器以外，还有一些用于通信数据转发的应用程序，例如代理、网关和隧道。它们可以配合服务器工作。
这些应用程序和服务器可以将请求转发给通信线路上的下一站服务器，并且能接收从那台服务器发送的响应再转发给客户端。
**代理**
代理是一种有转发功能的应用程序，它扮演了位于服务器和客户端“中间人”的角色，接收由客户端发送的请求并转发给服务器，同时也接收服务器返回的响应并转发给客户端。
**网关**
网关是转发其他服务器通信数据的服务器，接收从客户端发送来的请求时，它就像自己拥有资源的源服务器一样对请求进行处理。有时客户端可能都不会察觉，自己的通信目标是一个网关。
**隧道**
隧道是在相隔甚远的客户端和服务器两者之间进行中转，并保持双方通信连接的应用程序。
### 代理
代理服务器的基本行为就是接收客户端发送的请求后转发给其他服务器。代理不改变请求 URI，会直接发送给前方持有资源的目标服务器。
持有资源实体的服务器被称为源服务器。从源服务器返回的响应经过代理服务器后再传给客户端。
在 HTTP 通信过程中，可级联多台代理服务器。请求和响应的转发会经过数台类似锁链一样连接起来的代理服务器。转发时，需要附加 Via 首部字段以标记出经过的主机信息。
**缓存代理**
代理转发响应时，缓存代理（Caching Proxy）会预先将资源的副本（缓存）保存在代理服务器上。当代理再次接收到对相同资源的请求时，就可以不从源服务器那里获取资源，而是将之前缓存的资源作为响应返回。
**透明代理**
转发请求或响应时，不对报文做任何加工的代理类型被称为透明代理（Transparent Proxy）。反之，对报文内容进行加工的代理被称为非透明代理。
### 网关
网关的工作机制和代理十分相似。而网关能使通信线路上的服务器提供非 HTTP 协议服务。利用网关能提高通信的安全性，因为可以在客户端与网关之间的通信线路上加密以确保连接的安全。
###  隧道
隧道可按要求建立起一条与其他服务器的通信线路，届时使用 SSL 等加密手段进行通信。隧道的目的是确保客户端能与服务器进行安全的通信。
隧道本身不会去解析 HTTP 请求。也就是说，请求保持原样中转给之后的服务器。隧道会在通信双方断开连接时结束。
## 保存资源的缓存
缓存是指代理服务器或客户端本地磁盘内保存的资源副本。
缓存服务器是代理服务器的一种，并归类在缓存代理类型中。换句话说，当代理转发从服务器返回的响应时，代理服务器将会保存一份资源的副本。

# HTTP 首部
## HTTP 报文首部
<img src="img\屏幕截图 2022-12-05 103913.png">

HTTP 请求报文
<img src="img\屏幕截图 2022-12-05 104314.png">

下面的示例是访问 http://hackr.jp 时，请求报文的首部信息。
```s
GET / HTTP/1.1
Host: hackr.jp
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*; q=0.8
Accept-Language: ja,en-us;q=0.7,en;q=0.3
Accept-Encoding: gzip, deflate
DNT: 1
Connection: keep-alive
If-Modified-Since: Fri, 31 Aug 2007 02:02:20 GMT
If-None-Match: "45bae1-16a-46d776ac"
Cache-Control: max-age=
```
HTTP 响应报文
<img src="img\屏幕截图 2022-12-05 085135.png">

以下示例是之前请求访问 http://hackr.jp/ 时，返回的响应报文的首部信息。
```s
HTTP/1.1 304 Not Modified
Date: Thu, 07 Jun 2012 07:21:36 GMT
Server: Apache
Connection: close
Etag: "45bae1-16a-46d776ac"
```
## HTTP 首部字段
使用首部字段是为了给浏览器和服务器提供报文主体大小、所使用的语言、认证信息等内容。
### 4 种 HTTP 首部字段类型
HTTP 首部字段根据实际用途被分为以下 4 种类型。
**通用首部字段（General Header Fields）**
请求报文和响应报文两方都会使用的首部。
**请求首部字段（Request Header Fields）**
更多免费电子书请搜索「慧眼看」www.huiyankan.com
从客户端向服务器端发送请求报文时使用的首部。补充了请求的附加内容、客户端信息、响应内容相关优
先级等信息。
**响应首部字段（Response Header Fields）**
从服务器端向客户端返回响应报文时使用的首部。补充了响应的附加内容，也会要求客户端附加额外的内
容信息。
**实体首部字段（Entity Header Fields）**
针对请求报文和响应报文的实体部分使用的首部。补充了资源内容更新时间等与实体有关的信息。
### HTTP/1.1 首部字段一览
HTTP/1.1 规范定义了如下 47 种首部字段。
**通用首部字段**
|首部字段名| 说明|
|-----------------------|---------------------|
|Cache-Control |控制缓存的行为|
|Connection |逐跳首部、连接的管理|
|Date |创建报文的日期时间
|Pragma |报文指令
|Trailer| 报文末端的首部一览
|Transfer-Encoding| 指定报文主体的传输编码方式
|Upgrade |升级为其他协议
|Via |代理服务器的相关信息
|Warning| 错误通知
**请求首部字段**
|首部字段名 |说明
|-----------|----------------|
|Accept |用户代理可处理的媒体类型
|Accept-Charset |优先的字符集
|Accept-Encoding |优先的内容编码
|Accept-Language |优先的语言（自然语言）
|Authorization Web|认证信息
|Expect| 期待服务器的特定行为
|From| 用户的电子邮箱地址
|Host |请求资源所在服务器
|If-Match |比较实体标记（ETag）
|If-Modified-Since| 比较资源的更新时间
|If-None-Match |比较实体标记（与 If-Match 相反）
|If-Range| 资源未更新时发送实体 Byte 的范围请求
|If-Unmodified-Since |比较资源的更新时间（与If-Modified-Since相反）
|Max-Forwards |最大传输逐跳数
|Proxy-Authorization |代理服务器要求客户端的认证信息
|Range |实体的字节范围请求
|Referer |对请求中 URI 的原始获取方
|TE| 传输编码的优先级
|User-Agent| HTTP 客户端程序的信息
**响应首部字段**
|首部字段名 |说明|
|--------------|-----------|
|Accept-Ranges| 是否接受字节范围请求
|Age |推算资源创建经过时间
|ETag |资源的匹配信息
|Location| 令客户端重定向至指定URI
|Proxy-Authenticate |代理服务器对客户端的认证信息
|Retry-After| 对再次发起请求的时机要求
|Server| HTTP服务器的安装信息
|Vary |代理服务器缓存的管理信息
|WWW-Authenticate |服务器对客户端的认证信息
**实体首部字段**
|首部字段名 |说明|
|---------------|----------------|
|Allow |资源可支持的HTTP方法
|Content-Encoding| 实体主体适用的编码方式
|Content-Language |实体主体的自然语言
|Content-Length |实体主体的大小（单位：字节）
|Content-Location |替代对应资源的URI
|Content-MD5 |实体主体的报文摘要
|Content-Range |实体主体的位置范围
|Content-Type |实体主体的媒体类型
|Expires |实体主体过期的日期时间
|Last-Modified| 资源的最后修改日期时间
###  End-to-end 首部和 Hop-by-hop 首部
HTTP 首部字段将定义成缓存代理和非缓存代理的行为，分成 2 种类型。
端到端首部（End-to-end Header）分在此类别中的首部会转发给请求 / 响应对应的最终接收目标，且必须保存在由缓存生成的响应中，另
外规定它必须被转发。
逐跳首部（Hop-by-hop Header）
分在此类别中的首部只对单次转发有效，会因通过缓存或代理而不再转发。HTTP/1.1 和之后版本中，如果要使用 hop-by-hop 首部，需提供 Connection 首部字段。
下面列举了 HTTP/1.1 中的逐跳首部字段。除这 8 个首部字段之外，其他所有字段都属于端到端首部。
Connection
Keep-Alive
Proxy-Authenticate
Proxy-Authorization
Trailer
TE
Transfer-Encoding
Upgrad
## HTTP/1.1 通用首部字段
###  Cache-Control
**缓存请求指令**
|指令 |参数| 说明
|--------|---------|----------|
|no-cache |无| 强制向源服务器再次验证
|no-store |无 |不缓存请求或响应的任何内容
|max-age = [ 秒] |必需 |响应的最大Age值
|max-stale( = [ 秒]) |可省略| 接收已过期的响应
|min-fresh = [ 秒] |必需| 期望在指定时间内的响应仍有效
|no-transform |无 |代理不可更改媒体类型
|only-if-cached |无| 从缓存获取资源
|cache-extension |- |新指令标记（token）
**缓存响应指令**
|指令 |参数 |说明|
|---------------|--------------|-----------------|
|public| 无| 可向任意方提供响应的缓存
|private |可省略 |仅向特定用户返回响应
|no-cache |可省略 |缓存前必须先确认其有效性
|no-store| 无| 不缓存请求或响应的任何内容
|no-transform |无| 代理不可更改媒体类型
|must-revalidate |无| 可缓存但必须再向源服务器进行确认
|proxy-revalidate |无| 要求中间缓存服务器对缓存的响应有效性再进行确认
|max-age = [ 秒] |必需 |响应的最大Age值
|s-maxage = [ 秒] |必需| 公共缓存服务器响应的最大Age值
|cache-extension |- |新指令标记（token）
### Connection
Connection 首部字段具备如下两个作用。
**控制不再转发给代理的首部字段** Connection: Upgrade

**管理持久连接** Connection: close
### Date
首部字段 Date 表明创建 HTTP 报文的日期和时间
HTTP/1.1 协议使用在 RFC1123 中规定的日期时间的格式，如下 示例。
Date: Tue, 03 Jul 2012 04:40:59 GMT
### Pragma
Pragma 是 HTTP/1.1 之前版本的历史遗留字段，仅作为与 HTTP/1.0 的向后兼容而定义。
规范定义的形式唯一，如下所示。
Pragma: no-cache
该首部字段属于通用首部字段，但只用在客户端发送的请求中。客户端会要求所有的中间服务器不返回缓
存的资源。
所有的中间服务器如果都能以 HTTP/1.1 为基准，那直接采用 Cache-Control: no-cache 指定缓存的处
理方式是最为理想的。但要整体掌握全部中间服务器使用的 HTTP 协议版本却是不现实的。因此，发送的
请求会同时含有下面两个首部字段。
### Trailer
首部字段 Trailer 会事先说明在报文主体后记录了哪些首部字段。该首部字段可应用在 HTTP/1.1 版本分块传输编码时。
```s
HTTP/1.1 200 OK
Date: Tue, 03 Jul 2012 04:40:56 GMT
Content-Type: text/html
...
Transfer-Encoding: chunked
Trailer: Expires
...(报文主体)...
0
Expires: Tue, 28 Sep 2004 23:59:59 GMT
```
以上用例中，指定首部字段 Trailer 的值为 Expires，在报文主体之后（分块长度 0 之后）出现了首部字段 Expires。
### Transfer-Encoding
首部字段 Transfer-Encoding 规定了传输报文主体时采用的编码方式。
HTTP/1.1 的传输编码方式仅对分块传输编码有效。
```s
HTTP/1.1 200 OK
Date: Tue, 03 Jul 2012 04:40:56 GMT
Cache-Control: public, max-age=604800
Content-Type: text/javascript; charset=utf-8
Expires: Tue, 10 Jul 2012 04:40:56 GMT
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Content-Encoding: gzip
Transfer-Encoding: chunked
Connection: keep-alive
cf0 ←16进制(10进制为3312)
...3312字节分块数据...
392 ←16进制(10进制为914)
...914字节分块数据...
0
```
以上用例中，正如在首部字段 Transfer-Encoding 中指定的那样，有效使用分块传输编码，且分别被分成 3312 字节和 914 字节大小的分块数据。
### Upgrade
首部字段 Upgrade 用于检测 HTTP 协议及其他协议是否可使用更高的版本进行通信，其参数值可以用来指定一个完全不同的通信协议。
上图用例中，首部字段 Upgrade 指定的值为 TLS/1.0。请注意此处两个字段首部字段的对应关系，Connection 的值被指定为 Upgrade。Upgrade 首部字段产生作用的 Upgrade 对象仅限于客户端和邻接服务器之间。因此，使用首部字段 Upgrade 时，还需要额外指定 Connection:Upgrade。
对于附有首部字段 Upgrade 的请求，服务器可用 101 Switching Protocols 状态码作为响应返回。
### Via
使用首部字段 Via 是为了追踪客户端与服务器之间的请求和响应报文的传输路径。报文经过代理或网关时，会先在首部字段 Via 中附加该服务器的信息，然后再进行转发。这个做法和traceroute 及电子邮件的 Received 首部的工作机制很类似。
首部字段 Via 不仅用于追踪报文的转发，还可避免请求回环的发生。所以必须在经过代理时附加该首部字段内容。
###  Warning
该首部通常会告知用户一些与缓存相关的问题的警告。
Warning: [警告码][警告的主机:端口号]“[警告内容]”([日期时间])
HTTP/1.1 中定义了 7 种警告。警告码对应的警告内容仅推荐参考。
|警告码| 警告内容| 说明|
|------------|------------|-------------|
|110 |Response is stale（响应已过期）| 代理返回已过期的资源
|111 |Revalidation failed（再验证失败） |代理再验证资源有效性时失败（服务器无法到达等原因）
|112 |Disconnection operation（断开连接操作）| 代理与互联网连接被故意切断
|113 |Heuristic expiration（试探性过期） |响应的使用期超过24小时（有效缓存的设定时间大于24小
时的情况下）
|199 |Miscellaneous warning（杂项警告） |任意的警告内容
|214 |Transformation applied（使用了转换） |代理对内容编码或媒体类型等执行了某些处理时
|299| Miscellaneous persistent warning（持久杂项警告）| 任意的警告内容
## 请求首部字段
### Accept
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept 首部字段可通知服务器，用户代理能够处理的媒体类型及媒体类型的相对优先级。可使用
type/subtype 这种形式，一次指定多种媒体类型。
### Accept-Charset
Accept-Charset: iso-8859-5, unicode-1-1;q=0.8
Accept-Charset 首部字段可用来通知服务器用户代理支持的字符集及字符集的相对优先顺序。另外，可一次性指定多种字符集。与首部字段 Accept 相同的是可用权重 q 值来表示相对优先级。
该首部字段应用于内容协商机制的服务器驱动协商。
### Accept-Encoding
Accept-Encoding: gzip, deflate
Accept-Encoding 首部字段用来告知服务器用户代理支持的内容编码及内容编码的优先级顺序。可一次性
指定多种内容编码。
下面试举出几个内容编码的例子。
gzip
由文件压缩程序 gzip（GNU zip）生成的编码格式（RFC1952），采用 Lempel-Ziv 算法（LZ77）及
32 位循环冗余校验（Cyclic Redundancy Check，通称 CRC）。
compress
由 UNIX 文件压缩程序 compress 生成的编码格式，采用 Lempel-Ziv-Welch 算法（LZW）。
deflate
组合使用 zlib 格式（RFC1950）及由 deflate 压缩算法（RFC1951）生成的编码格式。
identity
不执行压缩或不会变化的默认编码格式
采用权重 q 值来表示相对优先级，这点与首部字段 Accept 相同。另外，也可使用星号（*）作为通配
符，指定任意的编码格式
### Accept-Language
Accept-Language: zh-cn,zh;q=0.7,en-us,en;q=0.3
首部字段 Accept-Language 用来告知服务器用户代理能够处理的自然语言集（指中文或英文等），以及自然语言集的相对优先级。可一次指定多种自然语言集。
### Authorization
Authorization: Basic dWVub3NlbjpwYXNzd29yZA==
首部字段 Authorization 是用来告知服务器，用户代理的认证信息（证书值）。通常，想要通过服务器认证的用户代理会在接收到返回的 401 状态码响应后，把首部字段 Authorization 加入请求中。共用缓存在接收到含有 Authorization 首部字段的请求时的操作处理会略有差异。
### Expect
Expect: 100-continue
客户端使用首部字段 Expect 来告知服务器，期望出现的某种特定行为。因服务器无法理解客户端的期望
作出回应而发生错误时，会返回状态码 417 Expectation Failed
###  From
首部字段 From 用来告知服务器使用用户代理的用户的电子邮件地址。通常，其使用目的就是为了显示搜索引擎等用户代理的负责人的电子邮件联系方式。使用代理时，应尽可能包含 From 首部字段（但可能会因代理不同，将电子邮件地址记录在 User-Agent 首部字段内）。
### Host
Host: www.hackr.jp
首部字段 Host 会告知服务器，请求的资源所处的互联网主机名和端口号。Host 首部字段在 HTTP/1.1规范内是唯一一个必须被包含在请求内的首部字段。
### If-Match
形如 If-xxx 这种样式的请求首部字段，都可称为条件请求。服务器接收到附带条件的请求后，只有判断指定条件为真时，才会执行请求。
图：只有当 If-Match 的字段值跟 ETag 值匹配一致时，服务器才会接受请求
If-Match: "123456"
首部字段 If-Match，属附带条件之一，它会告知服务器匹配资源所用的实体标记***（ETag）**值。这时的服务器无法使用弱 ETag 值。（请参照本章有关首部字段 ETag 的说明）
服务器会比对 If-Match 的字段值和资源的 ETag 值，仅当两者一致时，才会执行请求。反之，则返回状态码 412 Precondition Failed 的响应。还可以使用星号（*）指定 If-Match 的字段值。
### If-Modified-Since
图：如果在 If-Modified-Since 字段指定的日期时间后，资源发生了更新，服务器会接受请求
If-Modified-Since: Thu, 15 Apr 2004 00:00:00 GMT
首部字段 If-Modified-Since，属附带条件之一，它会告知服务器若 If-Modified-Since 字段值早于资源的更新时间，则希望能处理该请求。而在指定 If-Modified-Since 字段值的日期时间之后，如果请求
的资源都没有过更新，则返回状态码 304 Not Modified 的响应。
If-Modified-Since 用于确认代理或客户端拥有的本地资源的有效性。获取资源的更新日期时间，可通过确认首部字段 Last-Modified 来确定。
### If-None-Match
图：只有在 If-None-Match 的字段值与 ETag 值不一致时，可处理该请求。与 If-Match 首部字段的作用相反。
### If-Range
首部字段 If-Range 属于附带条件之一。它告知服务器若指定的 If-Range 字段值（ETag 值或者时间）和请求资源的 ETag 值或时间相一致时，则作为范围请求处理。反之，则返回全体资源。
### If-Unmodified-Since
If-Unmodified-Since: Thu, 03 Jul 2012 00:00:00 GMT
首部字段 If-Unmodified-Since 和首部字段 If-Modified-Since 的作用相反。它的作用的是告知服务器，指定的请求资源只有在字段值内指定的日期时间之后，未发生更新的情况下，才能处理请求。如果在
指定日期时间后发生了更新，则以状态码 412 Precondition Failed 作为响应返回。
### Max-Forwards
图：每次转发数值减 1。当数值变 0 时返回响应
Max-Forwards: 10

### Proxy-Authorization
Proxy-Authorization: Basic dGlwOjkpNLAGfFY5
接收到从代理服务器发来的认证质询时，客户端会发送包含首部字段 Proxy-Authorization 的请求，以告知服务器认证所需要的信息。
### Range
Range: bytes=5001-10000
对于只需获取部分资源的范围请求，包含首部字段 Range 即可告知服务器资源的指定范围。
接收到附带 Range 首部字段请求的服务器，会在处理请求之后返回状态码为 206 Partial Content 的响
应。无法处理该范围请求时，则会返回状态码 200 OK 的响应及全部资源。
### Referer
Referer: http://www.hackr.jp/index.htm
首部字段 Referer 会告知服务器请求的原始资源的 URI。
客户端一般都会发送 Referer 首部字段给服务器
### TE
TE: gzip, deflate;q=0.5
首部字段 TE 会告知服务器客户端能够处理响应的传输编码方式及相对优先级。它和首部字段 AcceptEncoding 的功能很相像，但是用于传输编码。
首部字段 TE 除指定传输编码之外，还可以指定伴随 trailer 字段的分块传输编码的方式。应用后者
时，只需把 trailers 赋值给该字段值。
TE: trailers
### User-Agent
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0.1
首部字段 User-Agent 会将创建请求的浏览器和用户代理名称等信息传达给服务器。
## 响应首部字段
### Accept-Ranges
Accept-Ranges: bytes
首部字段 Accept-Ranges 是用来告知客户端服务器是否能处理范围请求，以指定获取服务器端某个部分的资源。
可指定的字段值有两种，可处理范围请求时指定其为 bytes，反之则指定其为 none。
### Age
Age: 600
首部字段 Age 能告知客户端，源服务器在多久前创建了响应。字段值的单位为秒。
若创建该响应的服务器是缓存服务器，Age 值是指缓存后的响应再次发起认证到认证完成的时间值。代理创建响应时必须加上首部字段 Age。
### ETag
ETag: "82e22293907ce725faf67773957acd12"
首部字段 ETag 能告知客户端实体标识。它是一种可将资源以字符串形式做唯一性标识的方式。服务器会为每份资源分配对应的 ETag 值。
另外，当资源更新时，ETag 值也需要更新。生成 ETag 值时，并没有统一的算法规则，而仅仅是由服务器来分配。
资源被缓存时，就会被分配唯一性标识。例如，当使用中文版的浏览器访问 http://www.google.com/
时，就会返回中文版对应的资源，而使用英文版的浏览器访问时，则会返回英文版对应的资源。两者的
URI 是相同的，所以仅凭 URI 指定缓存的资源是相当困难的。若在下载过程中出现连接中断、再连接的情况，都会依照 ETag 值来指定资源。
强 ETag 值和弱 Tag 值
ETag 中有强 ETag 值和弱 ETag 值之分。
强 ETag 值
强 ETag 值，不论实体发生多么细微的变化都会改变其值。
ETag: "usagi-1234"
弱 ETag 值
弱 ETag 值只用于提示资源是否相同。只有资源发生了根本改变，产生差异时才会改变 ETag 值。
### Location
Location: http://www.usagidesign.jp/sample.html
使用首部字段 Location 可以将响应接收方引导至某个与请求 URI 位置不同的资源。
基本上，该字段会配合 3xx ：Redirection 的响应，提供重定向的 URI。
几乎所有的浏览器在接收到包含首部字段 Location 的响应后，都会强制性地尝试对已提示的重定向资源的访问。
### Proxy-Authenticate
Proxy-Authenticate: Basic realm="Usagidesign Auth"
首部字段 Proxy-Authenticate 会把由代理服务器所要求的认证信息发送给客户端。
它与客户端和服务器之间的 HTTP 访问认证的行为相似，不同之处在于其认证行为是在客户端与代理之间进行的。而客户端与服务器之间进行认证时，首部字段 WWW-Authorization 有着相同的作用。
### Retry-After
Retry-After: 120
首部字段 Retry-After 告知客户端应该在多久之后再次发送请求。主要配合状态码 503 Service Unavailable 响应，或 3xx Redirect 响应一起使用。字段值可以指定为具体的日期时间（Wed, 04 Jul 2012 06：34：24 GMT 等格式），也可以是创建响应后的秒数。
### Server
Server: Apache/2.2.17 (Unix)
首部字段 Server 告知客户端当前服务器上安装的 HTTP 服务器应用程序的信息。不单单会标出服务器上的软件应用名称，还有可能包括版本号和安装时启用的可选项。

### Vary
Vary: Accept-Language
首部字段 Vary 可对缓存进行控制。源服务器会向代理服务器传达关于本地缓存使用方法的命令。
从代理服务器接收到源服务器返回包含 Vary 指定项的响应之后，若再要进行缓存，仅对请求中含有相同Vary 指定首部字段的请求返回缓存。即使对相同资源发起请求，但由于 Vary 指定的首部字段不相同，因此必须要从源服务器重新获取资源。
### WWW-Authenticate
WWW-Authenticate: Basic realm="Usagidesign Auth"
首部字段 WWW-Authenticate 用于 HTTP 访问认证。它会告知客户端适用于访问请求 URI 所指定资源的认证方案（Basic 或是 Digest）和带参数提示的质询（challenge）。状态码 401 Unauthorized 响应
中，肯定带有首部字段 WWW-Authenticate。
###  实体首部字段
实体首部字段是包含在请求报文和响应报文中的实体部分所使用的首部，用于补充内容的更新时间等与实体相关的信息。
### Allow
Allow: GET, HEAD
首部字段 Allow 用于通知客户端能够支持 Request-URI 指定资源的所有 HTTP 方法。当服务器接收到不支持的 HTTP 方法时，会以状态码 405 Method Not Allowed 作为响应返回。与此同时，还会把所有能支
持的 HTTP 方法写入首部字段 Allow 后返回。
### Content-Encoding
Content-Encoding: gzip
首部字段 Content-Encoding 会告知客户端服务器对实体的主体部分选用的内容编码方式。内容编码是指在不丢失实体信息的前提下所进行的压缩。
主要采用以下 4 种内容编码的方式。（各方式的说明请参考 6.4.3 节 Accept-Encoding 首部字段）。
gzip
compress
deflate
identity
### Content-Language
Content-Language: zh-CN
首部字段 Content-Language 会告知客户端，实体主体使用的自然语言（指中文或英文等语言）。
### Content-Length
Content-Length: 15000
首部字段 Content-Length 表明了实体主体部分的大小（单位是字节）。对实体主体进行内容编码传输时，不能再使用 Content-Length 首部字段。由于实体主体大小的计算方法略微复杂，所以在此不再展
开。
### Content-Location
Content-Location: http://www.hackr.jp/index-ja.html
首部字段 Content-Location 给出与报文主体部分相对应的 URI。和首部字段 Location 不同，ContentLocation 表示的是报文主体返回资源对应的 URI。
### Content-MD5
Content-MD5 的字段值比较
Content-MD5: OGFkZDUwNGVhNGY3N2MxMDIwZmQ4NTBmY2IyTY==
首部字段 Content-MD5 是一串由 MD5 算法生成的值，其目的在于检查报文主体在传输过程中是否保持完整，以及确认传输到达。
对报文主体执行 MD5 算法获得的 128 位二进制数，再通过 Base64 编码后将结果写入 Content-MD5 字段值。由于 HTTP 首部无法记录二进制值，所以要通过 Base64 编码处理。为确保报文的有效性，作为接
收方的客户端会对报文主体再执行一次相同的 MD5 算法。计算出的值与字段值作比较后，即可判断出报文主体的准确性。采用这种方法，对内容上的偶发性改变是无从查证的，也无法检测出恶意篡改。其中一个原因在于，内容如果能够被篡改，那么同时意味着 Content-MD5 也可重新计算然后被篡改。所以处在接收阶段的客户端是无法意识到报文主体以及首部字段 Content-MD5 是已经被篡改过的。
### Content-Range
Content-Range: bytes 5001-10000/10000
针对范围请求，返回响应时使用的首部字段 Content-Range，能告知客户端作为响应返回的实体的哪个部
### Content-Type
Content-Type: text/html; charset=UTF-8
首部字段 Content-Type 说明了实体主体内对象的媒体类型。和首部字段 Accept 一样，字段值用
type/subtype 形式赋值。
参数 charset 使用 iso-8859-1 或 euc-jp 等字符集进行赋值。
### Expires
Expires: Wed, 04 Jul 2012 08:26:05 GMT
首部字段 Expires 会将资源失效的日期告知客户端。缓存服务器在接收到含有首部字段 Expires 的响应后，会以缓存来应答请求，在Expires 字段值指定的时间之前，响应的副本会一直被保存。当超过指定的时间后，缓存服务器在请求发送过来时，会转向源服务器请求资源。源服务器不希望缓存服务器对资源缓存时，最好在 Expires 字段内写入与首部字段 Date 相同的时间值。
但是，当首部字段 Cache-Control 有指定 max-age 指令时，比起首部字段 Expires，会优先处理 maxage 指令。
### Last-Modified
Last-Modified: Wed, 23 May 2012 09:59:55 GMT
首部字段 Last-Modified 指明资源最终修改的时间。
## 为 Cookie 服务的首部字段
Cookie 的工作机制是用户识别及状态管理。Web 网站为了管理用户的状态会通过 Web 浏览器，把一些数据临时写入用户的计算机内。接着当用户访问该Web网站时，可通过通信方式取回之前发放的 Cookie。

|首部字段名| 说明| 首部类型|
|----------|----------|-------------|
|Set-Cookie |开始状态管理所使用的Cookie信息 |响应首部字段|
|Cookie |服务器接收到的Cookie信息| 请求首部字段
### Set-Cookie
Set-Cookie: status=enable; expires=Tue, 05 Jul 2011 07:26:31 GMT; path=/; domain=.hackr.jp;
当服务器准备开始管理客户端的状态时，会事先告知各种信息。
下面的表格列举了 Set-Cookie 的字段值。
|属性 |说明|
|----------|---------|
|NAME=VALUE |赋予 Cookie 的名称和其值（必需项）|
|expires=DATE |Cookie 的有效期（若不明确指定则默认为浏览器关闭前为止）
|path=PATH |将服务器上的文件目录作为Cookie的适用对象（若不指定则默认为文档所在的文件目录）
|domain=域名 |作为 Cookie 适用对象的域名 （若不指定则默认为创建 Cookie 的服务器的域名）
|Secure |仅在 HTTPS 安全通信时才会发送 Cookie
|HttpOnly |加以限制，使 Cookie 不能被 JavaScript 脚本访问**expires 属性**
Cookie 的 expires 属性指定浏览器可发送 Cookie 的有效期。当省略 expires 属性时，其有效期仅限于维持浏览器会话（Session）时间段内。这通常限于浏览器应用程序被关闭之前。
另外，一旦 Cookie 从服务器端发送至客户端，服务器端就不存在可以显式删除 Cookie 的方法。但可通过覆盖已过期的 Cookie，实现对客户端 Cookie 的实质性删除操作。
**path 属性**
Cookie 的 path 属性可用于限制指定 Cookie 的发送范围的文件目录。不过另有办法可避开这项限制.
**domain 属性**
通过 Cookie 的 domain 属性指定的域名可做到与结尾匹配一致。比如，当指定 example.com 后，除example.com 以外，www.example.com 或 www2.example.com 等都可以发送 Cookie。
**secure 属性**
Cookie 的 secure 属性用于限制 Web 页面仅在 HTTPS 安全连接时，才可以发送 Cookie。
**HttpOnly 属性**
Cookie 的 HttpOnly 属性是 Cookie 的扩展功能，它使 JavaScript 脚本无法获得 Cookie。其主要目的为防止跨站脚本攻击（Cross-site scripting，XSS）对 Cookie 的信息窃取。
### Cookie
Cookie: status=enable
首部字段 Cookie 会告知服务器，当客户端想获得 HTTP 状态管理支持时，就会在请求中包含从服务器接收到的 Cookie。接收到多个 Cookie 时，同样可以以多个 Cookie 形式发送。

## 其他首部字段
HTTP 首部字段是可以自行扩展的。所以在 Web 服务器和浏览器的应用上，会出现各种非标准的首部字段。
接下来，我们就一些最为常用的首部字段进行说明。
X-Frame-Options
X-XSS-Protection
DNT
P3P
### X-Frame-Options
X-Frame-Options: DENY
首部字段 X-Frame-Options 属于 HTTP 响应首部，用于控制网站内容在其他 Web 网站的 Frame 标签内的显示问题。其主要目的是为了防止点击劫持（clickjacking）攻击。
首部字段 X-Frame-Options 有以下两个可指定的字段值。
DENY ：拒绝
SAMEORIGIN ：仅同源域名下的页面（Top-level-browsing-context）匹配时许可
### X-XSS-Protection
X-XSS-Protection: 1
首部字段 X-XSS-Protection 属于 HTTP 响应首部，它是针对跨站脚本攻击（XSS）的一种对策，用于控制浏览器 XSS 防护机制的开关。
首部字段 X-XSS-Protection 可指定的字段值如下。
0 ：将 XSS 过滤设置成无效状态
1 ：将 XSS 过滤设置成有效状态
### DNT
DNT: 1
首部字段 DNT 属于 HTTP 请求首部，其中 DNT 是 Do Not Track 的简称，意为拒绝个人信息被收集，是表示拒绝被精准广告追踪的一种方法。
首部字段 DNT 可指定的字段值如下。
0 ：同意被追踪
1 ：拒绝被追踪
由于首部字段 DNT 的功能具备有效性，所以 Web 服务器需要对 DNT 做对应的支持。
### P3P
P3P: CP="CAO DSP LAW CURa ADMa DEVa TAIa PSAa PSDa IVAa IVDa OUR BUS IND UNI COM NAV INT"
首部字段 P3P 属于 HTTP 相应首部，通过利用 P3P（The Platform for Privacy Preferences，在线隐私偏好平台）技术，可以让 Web 网站上的个人隐私变成一种仅供程序可理解的形式，以达到保护用户隐
私的目的。
要进行 P3P 的设定，需按以下操作步骤进行。
步骤 1：创建 P3P 隐私
步骤 2：创建 P3P 隐私对照文件后，保存命名在 /w3c/p3p.xml
步骤 3：从 P3P 隐私中新建 Compact policies 后，输出到 HTTP 响应中
有关 P3P 的详细规范标准请参看下方链接。
The Platform for Privacy Preferences 1.0（P3P1.0）Specification
http://www.w3.org/TR/P3P/
# 确保 Web 安全的 HTTPS
## HTTP 的缺点
HTTP 主要有这些不足，例举如下。
- 通信使用明文（不加密），内容可能会被窃听
- 不验证通信方的身份，因此有可能遭遇伪装
- 无法证明报文的完整性，所以有可能已遭篡改
### 通信使用明文可能会被窃听
- TCP/IP 是可能被窃听的网络
<img src="img\屏幕截图 2022-12-05 145708.png">

窃听相同段上的通信并非难事。只需要收集在互联网上流动的数据包（帧）就行了。对于收集来的数据包的解析工作，可交给那些抓包（Packet Capture）或嗅探器（Sniffer）工具。

- **加密处理防止被窃听**
在目前大家正在研究的如何防止窃听保护信息的几种对策中，最为普及的就是加密技术。加密的对象可以有这么几个。
**通信的加密**
一种方式就是将通信加密。HTTP 协议中没有加密机制，但可以通过和 SSL（Secure Socket Layer，安全套接层）或 TLS（Transport Layer Security，安全层传输协议）的组合使用，加密 HTTP 的通
信内容。
用 SSL 建立安全通信线路之后，就可以在这条线路上进行 HTTP 通信了。与 SSL 组合使用的 HTTP被称为 HTTPS（HTTP Secure，超文本传输安全协议）或 HTTP over SSL。
**内容的加密**
还有一种将参与通信的内容本身加密的方式。由于 HTTP 协议中没有加密机制，那么就对 HTTP 协议传输的内容本身加密。即把 HTTP 报文里所含的内容进行加密处理。在这种情况下，客户端需要对 HTTP 报文进行加密处理后再发送请求。诚然，为了做到有效的内容加密，前提是要求客户端和服务器同时具备加密和解密机制。主要应用在Web 服务中。有一点必须引起注意，由于该方式不同于 SSL 或 TLS 将整个通信线路加密处理，所以内容仍有被篡改的风险。稍后我们会加以说明。
### 不验证通信方的身份就可能遭遇伪装
HTTP 协议中的请求和响应不会对通信方进行确认。也就是说存在“服务器是否就是发送请求中 URI 真正指定的主机，返回的响应是否真的返回到实际提出请求的客户端”等类似问题。
- **任何人都可发起请求**
在 HTTP 协议通信时，由于不存在确认通信方的处理步骤，任何人都可以发起请求。另外，服务器只要接收到请求，不管对方是谁都会返回一个响应（但也仅限于发送端的 IP 地址和端口号没有被 Web
服务器设定限制访问的前提下）。
下各种隐患。
- 无法确定请求发送至目标的 Web 服务器是否是按真实意图返回响应的那台服务器。有可能是已伪装的 Web 服务器。
- 无法确定响应返回到的客户端是否是按真实意图接收响应的那个客户端。有可能是已伪装的客户端。
- 无法确定正在通信的对方是否具备访问权限。因为某些 Web 服务器上保存着重要的信息，只想发给特定用户通信的权限。
- 无法判定请求是来自何方、出自谁手。
即使是无意义的请求也会照单全收。无法阻止海量请求下的 DoS 攻击（Denial of Service，拒绝服务攻击）。
- **查明对手的证书**
虽然使用 HTTP 协议无法确定通信方，但如果使用 SSL 则可以。SSL 不仅提供加密处理，而且还使用了一种被称为证书的手段，可用于确定方。
证书由值得信任的第三方机构颁发，用以证明服务器和客户端是实际存在的。另外，伪造证书从技术角度来说是异常困难的一件事。所以只要能够确认通信方（服务器或客户端）持有的证书，即可判断通信方的真实意图。
通过使用证书，以证明通信方就是意料中的服务器。这对使用者个人来讲，也减少了个人信息泄露的危险性。
### 无法证明报文完整性，可能已遭篡改
所谓完整性是指信息的准确度。若无法证明其完整性，通常也就意味着无法判断信息是否准确。
- **接收到的内容可能有误**
由于 HTTP 协议无法证明通信的报文完整性，因此，在请求或响应送出之后直到对方接收之前的这段时间内，即使请求或响应的内容遭到篡改，也没有办法获悉。
换句话说，没有任何办法确认，发出的请求 / 响应和接收到的请求 / 响应是前后相同的。
比如，从某个 Web 网站上下载内容，是无法确定客户端下载的文件和服务器上存放的文件是否前后一致的。文件内容在传输途中可能已经被篡改为其他的内容。即使内容真的已改变，作为接收方的客户端也是觉察不到的。
像这样，请求或响应在传输途中，遭攻击者拦截并篡改内容的攻击称为中间人攻击（Man-in-theMiddle attack，MITM）。

- 如何防止篡改
虽然有使用 HTTP 协议确定报文完整性的方法，但事实上并不便捷、可靠。其中常用的是 MD5 和SHA-1 等散列值校验的方法，以及用来确认文件的数字签名方法。
提供文件下载服务的 Web 网站也会提供相应的以 PGP（Pretty Good Privacy，完美隐私）创建的数字签名及 MD5 算法生成的散列值。PGP 是用来证明创建文件的数字签名，MD5 是由单向函数生成的散列值。不论使用哪一种方法，都需要操纵客户端的用户本人亲自检查验证下载的文件是否就是原来
服务器上的文件。浏览器无法自动帮用户检查。
可惜的是，用这些方法也依然无法百分百保证确认结果正确。因为 PGP 和 MD5 本身被改写的话，用户是没有办法意识到的。
为了有效防止这些弊端，有必要使用 HTTPS。SSL 提供认证和加密处理及摘要功能。仅靠 HTTP 确保

## HTTP+ 加密 + 认证 + 完整性保护 =HTTPS
### HTTP 加上加密处理和认证以及完整性保护后即是 HTTPS
如果在 HTTP 协议通信过程中使用未经加密的明文，比如在 Web 页面中输入信用卡号，如果这条通信线路遭到窃听，那么信用卡号就暴露了。
需要在 HTTP 上再加入加密处理和认证等机制。我们把添加了加密及认证机制的 HTTP 称为 HTTPS（HTTP Secure）。
7.2.2 HTTPS 是身披 SSL 外壳的 HTTP
HTTPS 并非是应用层的一种新协议。只是 HTTP 通信接口部分用 SSL（Secure Socket Layer）和TLS（Transport Layer Security）协议代替而已。
<img src="img\屏幕截图 2022-12-05 151948.png">

### 相互交换密钥的公开密钥加密技术
在对 SSL 进行讲解之前，我们先来了解一下加密方法。SSL 采用一种叫做公开密钥加密（Public-keycryptography）的加密处理方式。
近代的加密方法中加密算法是公开的，而密钥却是保密的。通过这种方式得以保持加密方法的安全性。
- 共享密钥加密的困境
加密和解密同用一个密钥的方式称为共享密钥加密（Common key crypto system），也被叫做对称密钥加密。
- 使用两把密钥的公开密钥加密
公开密钥加密方式很好地解决了共享密钥加密的困难。
公开密钥加密使用一对非对称的密钥。一把叫做私有密钥（private key），另一把叫做公开密钥（public key）。顾名思义，私有密钥不能让其他任何人知道，而公开密钥则可以随意发布，任何人都可以获得。
使用公开密钥加密方式，发送密文的一方使用对方的公开密钥进行加密处理，对方收到被加密的信息后，再使用自己的私有密钥进行解密。利用这种方式，不需要发送用来解密的私有密钥，也不必担心密钥被攻击者窃听而盗走。

- HTTPS 采用混合加密机制
HTTPS 采用共享密钥加密和公开密钥加密两者并用的混合加密机制。若密钥能够实现安全交换，那么有可能会考虑仅使用公开密钥加密来通信。但是公开密钥加密与共享密钥加密相比，其处理速度要慢。
所以应充分利用两者各自的优势，将多种方法组合起来用于通信。在交换密钥环节使用公开密钥加密
方式，之后的建立通信交换报文阶段则使用共享密钥加密方式。

### 证明公开密钥正确性的证书
遗憾的是，公开密钥加密方式还是存在一些问题的。那就是无法证明公开密钥本身就是货真价实的公开密钥。
为了解决上述问题，可以使用由数字证书认证机构（CA，Certificate Authority）和其相关机关颁发的公开密钥证书。
首先，服务器的运营人员向数字证书认证机构提出公开密钥的申请。数字证书认证机构在判明提出申请者的身份之后，会对已申请的公开密钥做数字签名，然后分配这个已签名的公开密钥，并将该公开密钥放入公钥证书后绑定在一起。
服务器会将这份由数字证书认证机构颁发的公钥证书发送给客户端，以进行公开密钥加密方式通信。公钥证书也可叫做数字证书或直接称为证书。
接到证书的客户端可使用数字证书认证机构的公开密钥，对那张证书上的数字签名进行验证，一旦验证通过，客户端便可明确两件事：一，认证服务器的公开密钥的是真实有效的数字证书认证机构。二，服务器的公开密钥是值得信赖的。
此处认证机关的公开密钥必须安全地转交给客户端。使用通信方式时，如何安全转交是一件很困难的事，
因此，多数浏览器开发商发布版本时，会事先在内部植入常用认证机关的公开密钥。
- **可证明组织真实性的 EV SSL 证书**
证书的一个作用是用来证明作为通信一方的服务器是否规范，另外一个作用是可确认对方服务器背后运营的企业是否真实存在。拥有该特性的证书就是 EV SSL 证书（Extended Validation SSL
Certificate）。
EV SSL 证书是基于国际标准的认证指导方针颁发的证书。其严格规定了对运营组织是否真实的确认方针，因此，通过认证的 Web 网站能够获得更高的认可度。

- **用以确认客户端的客户端证书**
HTTPS 中还可以使用客户端证书。以客户端证书进行客户端认证，证明服务器正在通信的对方始终是预料之内的客户端，其作用跟服务器证书如出一辙。
- **认证机构信誉第一**
- **由自认证机构颁发的证书称为自签名证书**
如果使用 OpenSSL 这套开源程序，每个人都可以构建一套属于自己的认证机构，从而自己给自己颁发服务器证书。但该服务器证书在互联网上不可作为证书使用，似乎没什么帮助。
独立构建的认证机构叫做自认证机构，由自认证机构颁发的“无用”证书也被戏称为自签名证书。
浏览器访问该服务器时，会显示“无法确认连接安全性”或“该网站的安全证书存在问题”等警告消息。
### HTTPS 的安全通信机制
为了更好地理解 HTTPS，我们来观察一下 HTTPS 的通信步骤。
<img src="img\屏幕截图 2022-12-05 154353.png">

步骤 1： 客户端通过发送 Client Hello 报文开始 SSL 通信。报文中包含客户端支持的 SSL 的指定版本、加密组件（Cipher Suite）列表（所使用的加密算法及密钥长度等）。
步骤 2： 服务器可进行 SSL 通信时，会以 Server Hello 报文作为应答。和客户端一样，在报文中包含
SSL 版本以及加密组件。服务器的加密组件内容是从接收到的客户端加密组件内筛选出来的。
步骤 3： 之后服务器发送 Certificate 报文。报文中包含公开密钥证书。
步骤 4： 最后服务器发送 Server Hello Done 报文通知客户端，最初阶段的 SSL 握手协商部分结束。
步骤 5： SSL 第一次握手结束之后，客户端以 Client Key Exchange 报文作为回应。报文中包含通信加
密中使用的一种被称为 Pre-master secret 的随机密码串。该报文已用步骤 3 中的公开密钥进行加密。
步骤 6： 接着客户端继续发送 Change Cipher Spec 报文。该报文会提示服务器，在此报文之后的通信会采用 Pre-master secret 密钥加密。
步骤 7： 客户端发送 Finished 报文。该报文包含连接至今全部报文的整体校验值。这次握手协商是否
能够成功，要以服务器是否能够正确解密该报文作为判定标准。
步骤 8： 服务器同样发送 Change Cipher Spec 报文。
更多免费电子书请搜索「慧眼看」www.huiyankan.com
步骤 9： 服务器同样发送 Finished 报文。
步骤 10： 服务器和客户端的 Finished 报文交换完毕之后，SSL 连接就算建立完成。当然，通信会受到SSL 的保护。从此处开始进行应用层协议的通信，即发送 HTTP 请求。
步骤 11： 应用层协议通信，即发送 HTTP 响应。
步骤 12： 最后由客户端断开连接。断开连接时，发送 close_notify 报文。上图做了一些省略，这步之
后再发送 TCP FIN 报文来关闭与 TCP 的通信。
在以上流程中，应用层发送数据时会附加一种叫做 MAC（Message Authentication Code）的报文摘要。
MAC 能够查知报文是否遭到篡改，从而保护报文的完整性。
<img src="img\屏幕截图 2022-12-05 154833.png">

- **SSL 和 TLS**
HTTPS 使用 SSL（Secure Socket Layer） 和 TLS（Transport Layer Security）这两个协议。
- **SSL 速度慢吗**
HTTPS 也存在一些问题，那就是当使用 SSL 时，它的处理速度会变慢。
图：HTTPS 比 HTTP 要慢 2 到 100 倍
SSL 的慢分两种。一种是指通信慢。另一种是指由于大量消耗 CPU 及内存等资源，导致处理速度变慢。和使用 HTTP 相比，网络负载可能会变慢 2 到 100 倍。除去和 TCP 连接、发送 HTTP 请求 • 响应
以外，还必须进行 SSL 通信，因此整体上处理通信量不可避免会增加。
另一点是 SSL 必须进行加密处理。在服务器和客户端都需要进行加密和解密的运算处理。因此从结果上讲，比起 HTTP 会更多地消耗服务器和客户端的硬件资源，导致负载增强。针对速度变慢这一问题，并没有根本性的解决方案，我们会使用 SSL 加速器这种（专用服务器）硬件来改善该问题。该硬件为 SSL 通信专用硬件，相对软件来讲，能够提高数倍 SSL 的计算速度。仅在 SSL 处理时发挥 SSL 加速器的功效，以分担负载。
# 确认访问用户身份的认证
## 何为认证
**核对的信息通常是指以下这些**
密码：只有本人才会知道的字符串信息。
动态令牌：仅限本人持有的设备内显示的一次性密码。
数字证书：仅限本人（终端）持有的信息。
生物认证：指纹和虹膜等本人的生理信息。
IC 卡等：仅限本人持有的信息。
但是，即便对方是假冒的用户，只要能通过用户验证，那么计算机就会默认是出自本人的行为。因此，掌控机密信息的密码绝不能让他人得到，更不能轻易地就被破解出来。
**HTTP 使用的认证方式**
BASIC 认证（基本认证）
DIGEST 认证（摘要认证）
SSL 客户端认证
FormBase 认证（基于表单认证）

## BASIC 认证
BASIC 认证（基本认证）是从 HTTP/1.0 就定义的认证方式。即便是现在仍有一部分的网站会使用这种认证方式。是 Web 服务器与通信客户端之间进行的认证方式。
BASIC 认证的认证步骤
图：BASIC 认证概要
<img src="img\屏幕截图 2022-12-05 163332.png">

步骤 1： 当请求的资源需要 BASIC 认证时，服务器会随状态码 401 Authorization Required，返回带
WWW-Authenticate 首部字段的响应。该字段内包含认证的方式（BASIC） 及 Request-URI 安全域字符串（realm）。
步骤 2： 接收到状态码 401 的客户端为了通过 BASIC 认证，需要将用户 ID 及密码发送给服务器。发送的字符串内容是由用户 ID 和密码构成，两者中间以冒号（:）连接后，再经过 Base64 编码处理。
假设用户 ID 为 guest，密码是 guest，连接起来就会形成 guest:guest 这样的字符串。然后经过Base64 编码，最后的结果即是 Z3Vlc3Q6Z3Vlc3Q=。把这串字符串写入首部字段 Authorization 后，发送请求。
步骤 3： 接收到包含首部字段 Authorization 请求的服务器，会对认证信息的正确性进行验证。如验证通过，则返回一条包含 Request-URI 资源的响应。

BASIC 认证虽然采用 Base64 编码方式，但这不是加密处理。不需要任何附加信息即可对其解码。换言之，由于明文解码后就是用户 ID 和密码，在 HTTP 等非加密通信的线路上进行 BASIC 认证的过程中，
如果被人窃听，被盗的可能性极高。
另外，除此之外想再进行一次 BASIC 认证时，一般的浏览器却无法实现认证注销操作，这也是问题之一。

## DIGEST 认证
为弥补 BASIC 认证存在的弱点，从 HTTP/1.1 起就有了 DIGEST 认证。 DIGEST 认证同样使用质询 / 响应的方式（challenge/response），但不会像 BASIC 认证那样直接发送明文密码。
所谓质询响应方式是指，一开始一方会先发送认证要求给另一方，接着使用从另一方那接收到的质询码计算生成响应码。最后将响应码返回给对方进行认证的方式。
DIGEST 认证的认证步骤
图：DIGEST 认证概要
<img src="img\屏幕截图 2022-12-05 163619.png">

步骤 1： 请求需认证的资源时，服务器会随着状态码 401 Authorization Required，返 回带 WWWAuthenticate 首部字段的响应。该字段内包含质问响应方式认证所需的临时质询码（随机数，nonce）。
首部字段 WWW-Authenticate 内必须包含 realm 和 nonce 这两个字段的信息。客户端就是依靠向服务器回送这两个值进行认证的。
nonce 是一种每次随返回的 401 响应生成的任意随机字符串。该字符串通常推荐由 Base64 编码的十六进制数的组成形式，但实际内容依赖服务器的具体实现。
步骤 2： 接收到 401 状态码的客户端，返回的响应中包含 DIGEST 认证必须的首部字段 Authorization信息。
首部字段 Authorization 内必须包含 username、realm、nonce、uri 和 response 的字段信息。其中，realm 和 nonce 就是之前从服务器接收到的响应中的字段。
username 是 realm 限定范围内可进行认证的用户名。
uri（digest-uri）即 Request-URI 的值，但考虑到经代理转发后 Request-URI 的值可能被修改，因此事先会复制一份副本保存在 uri 内。
response 也可叫做 Request-Digest，存放经过 MD5 运算后的密码字符串，形成响应码。
步骤 3： 接收到包含首部字段 Authorization 请求的服务器，会确认认证信息的正确性。认证通过后则返回包含 Request-URI 资源的响应。
并且这时会在首部字段 Authentication-Info 写入一些认证成功的相关信息。
DIGEST 认证提供了高于 BASIC 认证的安全等级，但是和 HTTPS 的客户端认证相比仍旧很弱。DIGEST 认证提供防止密码被窃听的保护机制，但并不存在防止用户伪装的保护机制。
## SSL 客户端认证
从使用用户 ID 和密码的认证方式方面来讲，只要二者的内容正确，即可认证是本人的行为。但如果用户ID 和密码被盗，就很有可能被第三者冒充。利用 SSL 客户端认证则可以避免该情况的发生。
SSL 客户端认证是借由 HTTPS 的客户端证书完成认证的方式。凭借客户端证书认证，服务器可确认访问是否来自已登录的客户端。
### SSL 客户端认证的认证步骤
为达到 SSL 客户端认证的目的，需要事先将客户端证书分发给客户端，且客户端必须安装此证书。
步骤 1： 接收到需要认证资源的请求，服务器会发送 Certificate Request 报文，要求客户端提供客户端证书。
步骤 2： 用户选择将发送的客户端证书后，客户端会把客户端证书信息以 Client Certificate 报文方式发送给服务器。
步骤 3： 服务器验证客户端证书验证通过后方可领取证书内客户端的公开密钥，然后开始 HTTPS 加密通信。
### SSL 客户端认证采用双因素认证
在多数情况下，SSL 客户端认证不会仅依靠证书完成认证，一般会和基于表单认证（稍后讲解）组合形成一种双因素认证（Two-factor authentication）来使用。所谓双因素认证就是指，认证过程中不仅需要密码这一个因素，还需要申请认证者提供其他持有信息，从而作为另一个因素，与其组合使用的认证方式。
换言之，第一个认证因素的 SSL 客户端证书用来认证客户端计算机，另一个认证因素的密码则用来确定这是用户本人的行为。通过双因素认证后，就可以确认是用户本人正在使用匹配正确的计算机访问服务器。
### 基于表单认证
基于表单的认证方法并不是在 HTTP 协议中定义的。客户端会向服务器上的 Web 应用程序发送登录信息（Credential），按登录信息的验证结果认证。
多数情况下，输入已事先登录的用户 ID（通常是任意字符串或邮件地址）和密码等登录信息后，发送给Web 应用程序，基于认证结果来决定认证是否成功。

### Session 管理及 Cookie 应用
基于表单认证的标准规范尚未有定论，一般会使用 Cookie 来管理 Session（会话）。
图：Session 管理及 Cookie 状态管理
<img src="img\屏幕截图 2022-12-05 164601.png">

步骤 1： 客户端把用户 ID 和密码等登录信息放入报文的实体部分，通常是以 POST 方法把请求发送给
服务器。而这时，会使用 HTTPS 通信来进行 HTML 表单画面的显示和用户输入数据的发送。
步骤 2： 服务器会发放用以识别用户的 Session ID。通过验证从客户端发送过来的登录信息进行身份认证，然后把用户的认证状态与 Session ID 绑定后记录在服务器端。向客户端返回响应时，会在首部字段 Set-Cookie 内写入 Session ID（如 PHPSESSID=028a8c…）。
你可以把 Session ID 想象成一种用以区分不同用户的等位号。
然而，如果 Session ID 被第三方盗走，对方就可以伪装成你的身份进行恶意操作了。因此必须防止Session ID 被盗，或被猜出。为了做到这点，Session ID 应使用难以推测的字符串，且服务器端也需要
进行有效期的管理，保证其安全性。另外，为减轻跨站脚本攻击（XSS）造成的损失，建议事先在 Cookie 内加上 httponly 属性。
步骤 3： 客户端接收到从服务器端发来的 Session ID 后，会将其作为 Cookie 保存在本地。下次向服务器发送请求时，浏览器会自动发送 Cookie，所以 Session ID 也随之发送到服务器。服务器端可通过
验证接收到的 Session ID 识别用户和其认证状态。
# 基于 HTTP 的功能追加协议
## 消除 HTTP 瓶颈的 SPDY
Google 在 2010 年发布了 SPDY（取自 SPeeDY，发音同 speedy），其开发目标旨在解决 HTTP 的性能瓶颈，缩短 Web 页面的加载时间（50%）。
SPDY - The Chromium Projects
http://www.chromium.org/spdy/
### HTTP 的瓶颈
**以下这些 HTTP 标准就会成为瓶颈**
- 一条连接上只可发送一个请求.
- 请求只能从客户端开始。客户端不可以接收除响应以外的指令。
- 请求 / 响应首部未经压缩就发送。首部信息越多延迟越大。
- 发送冗长的首部。每次互相发送相同的首部造成的浪费较多。
- 可任意选择数据压缩格式。非强制压缩发送。
图：以前的 HTTP 通信
<img src="img\屏幕截图 2022-12-05 165216.png">

**Ajax 的解决方法**
Ajax（Asynchronous JavaScript and XML， 异 步 JavaScript 与 XML 技术）是一种有效利用JavaScript 和 DOM（Document Object Model，文档对象模型）的操作，以达到局部 Web 页面替换加载的异步通信手段。和以前的同步通信相比，由于它只更新一部分页面，响应中传输的数据量会因此而减少，这一优点显而易见。Ajax 的核心技术是名为 XMLHttpRequest 的 API，通过JavaScript 脚本语言的调用就能和服务器进行HTTP 通信。借由这种手段，就能从已加载完毕的 Web 页面上发起请求，只更新局部页面。而利用 Ajax 实时地从服务器获取内容，有可能会导致大量请求产生。另外，Ajax 仍未解决 HTTP 协议本身存在的问题。
图：Ajax 通信
<img src="img\屏幕截图 2022-12-05 165637.png">

**Comet 的解决方法**
一旦服务器端有内容更新了，Comet 不会让请求等待，而是直接给客户端返回响应。这是一种通过延迟应答，模拟实现服务器端向客户端推送（Server Push）的功能。通常，服务器端接收到请求，在处理完毕后就会立即返回响应，但为了实现推送功能，Comet 会先将响应置于挂起状态，当服务器端有内容更新时，再返回该响应。因此，服务器端一旦有更新，就可以立即反馈给客户端。内容上虽然可以做到实时更新，但为了保留响应，一次连接的持续时间也变长了。期间，为了维持连接会消耗更多的资源。另外，Comet 也仍未解决 HTTP 协议本身存在的问题。
图：Comet 通信
<img src="img\屏幕截图 2022-12-05 165911.png">


### SPDY 的设计与功能
SPDY 没有完全改写 HTTP 协议，而是在 TCP/IP 的应用层与运输层之间通过新加会话层的形式运作。同时，考虑到安全性问题，SPDY 规定通信中使用 SSL。
SPDY 以会话层的形式加入，控制对数据的流动，但还是采用 HTTP 建立通信连接。因此，可照常使用HTTP 的 GET 和 POST 等方 法、Cookie 以及 HTTP 报文等。
图：SPDY 的设计
<img src="img\屏幕截图 2022-12-05 170150.png">

使用 SPDY 后，HTTP 协议额外获得以下功能。

- **多路复用流**
通过单一的 TCP 连接，可以无限制处理多个 HTTP 请求。所有请求的处理都在一条 TCP 连接上完成，因此 TCP 的处理效率得到提高。
- **赋予请求优先级**
SPDY 不仅可以无限制地并发处理请求，还可以给请求逐个分配优先级顺序。这样主要是为了在发送多个请求时，解决因带宽低而导致响应变慢的问题。
- **压缩 HTTP 首部**
压缩 HTTP 请求和响应的首部。这样一来，通信产生的数据包数量和发送的字节数就更少了。
- **推送功能**
支持服务器主动向客户端推送数据的功能。这样，服务器可直接发送数据，而不必等待客户端的请求。
- **服务器提示功能**
服务器可以主动提示客户端请求所需的资源。由于在客户端发现资源之前就可以获知资源的存在，因此在资源已缓存等情况下，可以避免发送不必要的请求。
## 使用浏览器进行全双工通信的 WebSocket

### WebSocket 的设计与功能
WebSocket，即 Web 浏览器与 Web 服务器之间全双工通信标准。其中，WebSocket 协议由 IETF 定为标
准，WebSocket API 由 W3C 定为标准。仍在开发中的 WebSocket 技术主要是为了解决 Ajax 和 Comet里 XMLHttpRequest 附带的缺陷所引起的问题。
### WebSocket 协议
一旦 Web 服务器与客户端之间建立起 WebSocket 协议的通信连接，之后所有的通信都依靠这个专用协议进行。通信过程中可互相发送 JSON、XML、HTML 或图片等任意格式的数据。
由于是建立在 HTTP 基础上的协议，因此连接的发起方仍是客户端，而一旦确立 WebSocket 通信连接，不论服务器还是客户端，任意一方都可直接向对方发送报文。
下面我们列举一下 WebSocket 协议的主要特点。
- **推送功能**
支持由服务器向客户端推送数据的推送功能。这样，服务器可直接发送数据，而不必等待客户端的请求。
- **减少通信量**
只要建立起 WebSocket 连接，就希望一直保持连接状态。和 HTTP 相比，不但每次连接时的总开销减少，而且由于 WebSocket 的首部信息很小，通信量也相应减少了。
为了实现 WebSocket 通信，在 HTTP 连接建立之后，需要完成一次“握手”（Handshaking）的步骤。
握手·请求
为了实现 WebSocket 通信，需要用到 HTTP 的 Upgrade 首部字段，告知服务器通信协议发生改变，
以达到握手的目的。
```s
GET /chat HTTP/1.1
Host: server.example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Origin: http://example.com
Sec-WebSocket-Protocol: chat, superchat
Sec-WebSocket-Version: 13
Sec-WebSocket-Key 字段内记录着握手过程中必不可少的键值。Sec-WebSocket-Protocol 字段内记
```
录使用的子协议。
子协议按 WebSocket 协议标准在连接分开使用时，定义那些连接的名称。
握手·响应
对于之前的请求，返回状态码 101 Switching Protocols 的响应。
```s
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
Sec-WebSocket-Protocol: chat
```
Sec-WebSocket-Accept 的字段值是由握手请求中的 Sec-WebSocket-Key 的字段值生成的。
成功握手确立 WebSocket 连接之后，通信时不再使用 HTTP 的数据帧，而采用 WebSocket 独立的数
据帧。
图：WebSocket 通信
<img src="img\屏幕截图 2022-12-05 171002.png">

- **WebSocket API**
JavaScript 可调用“The WebSocket API”（http://www.w3.org/TR/websockets/，由 W3C 标准制定）内提供的 WebSocket 程序接口，以实现 WebSocket 协议下全双工通信。
以下为调用 WebSocket API，每 50ms 发送一次数据的实例。
```javascript
var socket = new WebSocket('ws://game.example.com:12010/updates');
socket.onopen = function () {
setInterval(function() {
if (socket.bufferedAmount == 0)
socket.send(getUpdateData());
}, 50);
};
```
