Search.setIndex({docnames:["index","reference"],envversion:51,filenames:["index.rst","reference.rst"],objects:{"switchyard.lib":{userlib:[1,6,0,"-"]},"switchyard.lib.address":{EthAddr:[1,0,1,""],SpecialIPv4Addr:[1,0,1,""],SpecialIPv6Addr:[1,0,1,""]},"switchyard.lib.address.EthAddr":{isBridgeFiltered:[1,1,1,""],isGlobal:[1,1,1,""],isLocal:[1,1,1,""],isMulticast:[1,1,1,""],is_bridge_filtered:[1,2,1,""],is_global:[1,2,1,""],is_local:[1,2,1,""],is_multicast:[1,2,1,""],packed:[1,2,1,""],raw:[1,2,1,""],toRaw:[1,1,1,""],toStr:[1,1,1,""],toTuple:[1,1,1,""]},"switchyard.lib.debugging":{"debugger":[1,3,1,""]},"switchyard.lib.interface":{Interface:[1,0,1,""],InterfaceType:[1,0,1,""]},"switchyard.lib.interface.Interface":{ethaddr:[1,2,1,""],ifnum:[1,2,1,""],iftype:[1,2,1,""],ipaddr:[1,2,1,""],ipinterface:[1,2,1,""],name:[1,2,1,""],netmask:[1,2,1,""]},"switchyard.lib.logging":{log_debug:[1,3,1,""],log_failure:[1,3,1,""],log_info:[1,3,1,""],log_warn:[1,3,1,""]},"switchyard.lib.packet":{Arp:[1,0,1,""],Ethernet:[1,0,1,""],ICMP:[1,0,1,""],ICMPDestinationUnreachable:[1,0,1,""],ICMPEchoReply:[1,0,1,""],ICMPEchoRequest:[1,0,1,""],ICMPRedirect:[1,0,1,""],ICMPSourceQuench:[1,0,1,""],ICMPTimeExceeded:[1,0,1,""],ICMPv6:[1,0,1,""],ICMPv6NeighborAdvertisement:[1,0,1,""],ICMPv6NeighborSolicitation:[1,0,1,""],ICMPv6RedirectMessage:[1,0,1,""],IPv4:[1,0,1,""],IPv6:[1,0,1,""],Packet:[1,0,1,""],PacketHeaderBase:[1,0,1,""],TCP:[1,0,1,""],UDP:[1,0,1,""]},"switchyard.lib.packet.Arp":{hardwaretype:[1,2,1,""],operation:[1,2,1,""],protocoltype:[1,2,1,""],senderhwaddr:[1,2,1,""],senderprotoaddr:[1,2,1,""],targethwaddr:[1,2,1,""],targetprotoaddr:[1,2,1,""]},"switchyard.lib.packet.Ethernet":{dst:[1,2,1,""],ethertype:[1,2,1,""],src:[1,2,1,""]},"switchyard.lib.packet.ICMP":{icmpcode:[1,2,1,""],icmpdata:[1,2,1,""],icmptype:[1,2,1,""]},"switchyard.lib.packet.ICMPDestinationUnreachable":{data:[1,2,1,""],nexthopmtu:[1,2,1,""],origdgramlen:[1,2,1,""]},"switchyard.lib.packet.ICMPEchoReply":{data:[1,2,1,""],identifier:[1,2,1,""],sequence:[1,2,1,""]},"switchyard.lib.packet.ICMPEchoRequest":{data:[1,2,1,""],identifier:[1,2,1,""],sequence:[1,2,1,""]},"switchyard.lib.packet.ICMPRedirect":{data:[1,2,1,""],redirectto:[1,2,1,""]},"switchyard.lib.packet.ICMPSourceQuench":{data:[1,2,1,""]},"switchyard.lib.packet.ICMPTimeExceeded":{data:[1,2,1,""],origdgramlen:[1,2,1,""]},"switchyard.lib.packet.ICMPv6NeighborAdvertisement":{data:[1,2,1,""],get_rso_byte:[1,1,1,""],get_rso_str:[1,1,1,""],options:[1,2,1,""],overrideflag:[1,2,1,""],routerflag:[1,2,1,""],solicitedflag:[1,2,1,""],targetaddr:[1,2,1,""]},"switchyard.lib.packet.ICMPv6NeighborSolicitation":{data:[1,2,1,""],options:[1,2,1,""],targetaddr:[1,2,1,""]},"switchyard.lib.packet.ICMPv6RedirectMessage":{data:[1,2,1,""],destinationaddr:[1,2,1,""],options:[1,2,1,""],targetaddr:[1,2,1,""]},"switchyard.lib.packet.IPv4":{dscp:[1,2,1,""],dst:[1,2,1,""],ecn:[1,2,1,""],flags:[1,2,1,""],fragment_offset:[1,2,1,""],hl:[1,2,1,""],ipid:[1,2,1,""],options:[1,2,1,""],protocol:[1,2,1,""],src:[1,2,1,""],tos:[1,2,1,""],total_length:[1,2,1,""],ttl:[1,2,1,""]},"switchyard.lib.packet.IPv6":{dst:[1,2,1,""],flowlabel:[1,2,1,""],hopcount:[1,2,1,""],nextheader:[1,2,1,""],src:[1,2,1,""],trafficclass:[1,2,1,""],ttl:[1,2,1,""]},"switchyard.lib.packet.Packet":{add_header:[1,1,1,""],add_payload:[1,1,1,""],from_bytes:[1,4,1,""],get_header:[1,1,1,""],get_header_by_name:[1,1,1,""],get_header_index:[1,1,1,""],has_header:[1,1,1,""],headers:[1,1,1,""],insert_header:[1,1,1,""],num_headers:[1,1,1,""],prepend_header:[1,1,1,""],size:[1,1,1,""],to_bytes:[1,1,1,""]},"switchyard.lib.packet.PacketHeaderBase":{add_next_header_class:[1,5,1,""],from_bytes:[1,1,1,""],set_next_header_class_key:[1,5,1,""],set_next_header_map:[1,5,1,""],size:[1,1,1,""],to_bytes:[1,1,1,""]},"switchyard.lib.packet.TCP":{ACK:[1,2,1,""],CWR:[1,2,1,""],ECE:[1,2,1,""],FIN:[1,2,1,""],NS:[1,2,1,""],PSH:[1,2,1,""],RST:[1,2,1,""],SYN:[1,2,1,""],URG:[1,2,1,""],ack:[1,2,1,""],dst:[1,2,1,""],flags:[1,2,1,""],flagstr:[1,2,1,""],offset:[1,2,1,""],options:[1,2,1,""],seq:[1,2,1,""],src:[1,2,1,""],urgent_pointer:[1,2,1,""],window:[1,2,1,""]},"switchyard.lib.packet.UDP":{dst:[1,2,1,""],length:[1,2,1,""],src:[1,2,1,""]},"switchyard.lib.packet.common":{ArpOperation:[1,0,1,""],EtherType:[1,0,1,""],ICMPType:[1,0,1,""],IPProtocol:[1,0,1,""]},"switchyard.lib.packet.icmpv6":{ICMPv6Option:[1,0,1,""],ICMPv6OptionRedirectedHeader:[1,0,1,""],ICMPv6OptionSourceLinkLayerAddress:[1,0,1,""],ICMPv6OptionTargetLinkLayerAddress:[1,0,1,""]},"switchyard.lib.socket":{ApplicationLayer:[1,0,1,""],socket:[1,0,1,""]},"switchyard.lib.socket.ApplicationLayer":{recv_from_app:[1,4,1,""],send_to_app:[1,4,1,""]},"switchyard.lib.socket.socket":{accept:[1,1,1,""],bind:[1,1,1,""],close:[1,1,1,""],connect:[1,1,1,""],connect_ex:[1,1,1,""],family:[1,2,1,""],getpeername:[1,1,1,""],getsockname:[1,1,1,""],getsockopt:[1,1,1,""],gettimeout:[1,1,1,""],listen:[1,1,1,""],proto:[1,2,1,""],recv:[1,1,1,""],recv_into:[1,1,1,""],recvfrom:[1,1,1,""],recvfrom_into:[1,1,1,""],recvmsg:[1,1,1,""],send:[1,1,1,""],sendall:[1,1,1,""],sendmsg:[1,1,1,""],sendto:[1,1,1,""],setblocking:[1,1,1,""],setsockopt:[1,1,1,""],settimeout:[1,1,1,""],shutdown:[1,1,1,""],timeout:[1,2,1,""],type:[1,2,1,""]},"switchyard.lib.testing":{PacketInputEvent:[1,0,1,""],PacketInputTimeoutEvent:[1,0,1,""],PacketOutputEvent:[1,0,1,""],TestScenario:[1,0,1,""]},"switchyard.lib.testing.PacketInputEvent":{match:[1,1,1,""]},"switchyard.lib.testing.PacketInputTimeoutEvent":{match:[1,1,1,""]},"switchyard.lib.testing.PacketOutputEvent":{match:[1,1,1,""]},"switchyard.lib.testing.TestScenario":{add_file:[1,1,1,""],add_interface:[1,1,1,""],expect:[1,1,1,""],interfaces:[1,1,1,""],name:[1,2,1,""],ports:[1,1,1,""]},"switchyard.llnetbase":{LLNetBase:[1,0,1,""]},"switchyard.llnetbase.LLNetBase":{interface_by_ipaddr:[1,1,1,""],interface_by_macaddr:[1,1,1,""],interface_by_name:[1,1,1,""],interfaces:[1,1,1,""],port_by_ipaddr:[1,1,1,""],port_by_macaddr:[1,1,1,""],port_by_name:[1,1,1,""],ports:[1,1,1,""],recv_packet:[1,1,1,""],send_packet:[1,1,1,""],testmode:[1,2,1,""]}},objnames:{"0":["py","class","Python class"],"1":["py","method","Python method"],"2":["py","attribute","Python attribute"],"3":["py","function","Python function"],"4":["py","staticmethod","Python static method"],"5":["py","classmethod","Python class method"],"6":["py","module","Python module"]},objtypes:{"0":"py:class","1":"py:method","2":"py:attribute","3":"py:function","4":"py:staticmethod","5":"py:classmethod","6":"py:module"},terms:{"0x05dc":1,"0x0800":1,"0x0806":1,"0x104449c78":[],"0x104474248":[],"0x1044742c8":[],"0x10632bb08":1,"0x10d3a3308":1,"0x8100":1,"0x86dd":1,"0x8809":1,"0x8847":1,"0x88a8":1,"0x88cc":1,"0x88e7":1,"27ff":[],"2nd":[],"3du":[],"6sxb":[],"boolean":[],"break":[],"byte":1,"case":1,"catch":[],"char":1,"class":[],"default":1,"enum":1,"final":[],"function":0,"import":1,"int":[],"long":1,"new":[0,1],"null":[],"public":0,"return":1,"short":[],"static":1,"switch":1,"throw":[],"true":1,"try":1,"while":[],Adding:1,And:[],CNS:0,DNS:[],ECE:1,For:1,Its:[],LTS:[],Not:1,OSes:[],One:[],That:[],The:[0,1],There:1,These:1,Use:[],Used:[],Using:1,With:[],__class__:[],__init__:[],__name__:[],__str__:[],_hops_to_root:[],_net:[],_packfmt:[],_root:[],_sequenc:[],a00:[],abbrevi:[],abl:[],about:1,abov:1,accept:1,access:1,accomplish:[],accord:[],ack:1,acknowledg:0,acquaint:[],act:1,activ:[],actual:[],add:1,add_fil:1,add_head:1,add_interfac:1,add_next_header_class:1,add_payload:1,added:[],adding:[],addit:1,addr:1,address:0,administ:1,advanc:0,advantag:[],af_inet:[],after:1,again:[],against:[],alia:1,alias:[],all:1,all_nodes_interface_loc:1,all_nodes_link_loc:1,all_routers_interface_loc:1,all_routers_link_loc:1,allow:[],almost:[],alon:[],along:[],alphabet:1,alreadi:1,also:1,alter:1,altern:[],although:[],altq:[],alwai:[],among:[],ani:[0,1],anoth:[0,1],anyth:[],anywher:1,api:0,app:1,appdata:[],appear:[],append:1,applic:0,applicationlay:1,appreci:[],approach:[],appropri:1,apt:[],arbitrari:[],aren:[],arg:1,arglist:[],argument:[0,1],aris:[],around:[],arp:[],arpoper:1,arppacket:1,arriv:1,assembl:[],assert:[],assign:1,associ:1,assum:1,attach:1,attempt:[],attr:1,attribut:[0,1],author:0,automat:1,avail:1,avoid:[],awai:[],awar:[],baaadhub:[],back:[],backlog:1,backtick:[],backward:[],bail:[],barford:[],base:[0,1],basic:[0,1],bdb:[],becaus:[],becom:[],been:1,befor:1,begin:1,behav:[],behavior:[],being:1,belief:[],below:1,besid:[],best:[],between:1,bewar:[],big:[],bin:[],bind:1,bit:[],block:1,blue:[],both:[],branch:[],brew:[],bridg:1,brief:[],briefli:[],bring:[],broadcast:[],broken:[],bsd:[],buffers:1,bug:[],bugfix:[],build:[],built:1,builtin:1,bytestr:1,c11:[],c19:[],calcsiz:[],call:1,can:1,cannot:1,capabl:[],care:[],career:0,carefulli:[],carri:[],categori:[],caus:1,certain:[],certainli:[],chain:[],chang:1,channel:[],chapter:[],charact:1,check:[0,1],checksum:[],choic:[],choos:[],clariti:1,classmethod:1,classnam:[],clean:[],clear:[],clearli:[],click:[],client:[],clientapp_udpstackex:[],clone:[],close:1,code:[0,1],coerc:1,cohes:[],colgat:[],collect:[],color:[],com:[],come:1,command:0,comment:[],commod:[],common:[0,1],commun:1,communicationadministrativelyprohibit:1,compact:[],compar:[],compat:[],compil:0,complet:[],complex:[],compon:[],compos:[],concern:1,conclus:0,configur:1,conform:1,conjunct:[],connect:1,connect_ex:1,consid:1,consist:1,consol:[],constant:[],construct:0,constructor:[],consum:[],contain:1,content:1,context:[],continu:1,contrari:[],contribut:[],control:[],conveni:1,convent:[],convers:[],copi:[],copyfromlastout:1,core:[],correct:1,correctli:1,correspond:1,cosc465:[],could:[],couldn:[],coupl:[],cours:[],cover:[],coverag:0,craft:[],crash:[],creat:[0,1],create_connect:[],creation:0,creativ:0,creativecommon:0,creator:[],cretin:[],critic:[],cs640:[],current:1,cwr:1,cycl:[],data:1,date:[],daunt:[],deactiv:[],dead:1,deal:[],death:[],debug:1,debugg:1,decid:1,decod:[],decrement:[],def:[],defin:1,definit:1,del:1,delet:1,deliv:1,depend:[],dependend:[],depict:[],deriv:1,describ:[],descript:1,deseri:1,design:[],desktop:[],destin:1,destinationaddr:1,destinationhostunknown:1,destinationnetworkunknown:1,destinationunreach:1,detail:1,determin:1,dev:[],devel:[],develop:[],devic:1,devnam:[],diagnosi:[],diagram:[],dictionari:1,did:1,didn:1,differ:[],difficult:[],directli:1,directori:[],disabl:[],discourag:[],discov:[],discoveri:1,discuss:[],displai:1,distribut:0,document:1,doe:1,doesn:[],doing:[],domain:[],don:[0,1],done:1,down:1,download:[],dpt:[],drive:[],drop:[],dropbox:[],dscp:1,dst:1,dstip:1,due:[],dumb:[],dump:[],durat:[],dure:[],dynam:[],each:1,earlier:[],easi:1,easier:[],easiest:[],easili:[],easy_instal:[],echo:[],echorepli:1,echorequest:1,ecn:1,educ:[],effect:[],effort:[],either:1,element:[],ell:1,ellipsi:[],els:[],emit:1,emphas:[],emploi:[],empti:[],emul:[0,1],en0:[],en1:[],en2:[],enabl:[],encapsul:1,end:1,endian:[],enforc:1,enhanc:[],enough:[],enp0s3:[],ensur:[],enter:[],enterdebugg:[],entir:[],entri:1,entrypoint:[],enumer:1,env:[],environ:0,eof:[],ephemer:[],equival:[],erron:[],error:1,especi:[],establish:[],etc:[],eth0:[],eth1:[],eth2:[],eth:[],ethaddr:1,ether:1,ethernet:0,ethertyp:1,eval:[],even:0,event:1,event_output:[],eventu:[],ever:[],everi:[],everyth:[],evtyp:1,exact:[],exactli:[],exampl:[0,1],except:1,exclud:0,execut:[],exercis:[],exist:1,exit:[],expand:0,expans:[],expect:1,expectation_object:[],experi:[],expir:[],explanatori:[],explicit:[],explicitli:[],express:0,extens:[],extent:1,facil:[],facilit:1,fact:[],fail:[0,1],failur:1,fals:1,famili:1,familiar:[],far:[],fate:[],favor:[],fe80:[],featur:1,febb:[],feedback:[],few:[],ff01:1,ff02:1,field:1,figur:[],file:[],filenam:[],fileno:1,fill:[],filter:1,fin:1,find:0,fine:[],finish:[],firewal:0,first:1,first_head:1,fix:[],flag:1,flagstr:1,flaw:[],flood:[],flow:[],flowaddr:1,flowlabel:1,fname:1,focu:[],folder:[],follow:1,fool:[],foolishli:[],footnot:[],forc:[],form:[],format:1,forward:[],forwarding_t:[],found:1,foundat:0,four:[],fragment_offset:1,fragmentationrequireddfset:1,frame:1,framework:1,from:[0,1],from_byt:1,full:0,fulli:[],fun:[],furthermor:[],futur:[],gain:[],gather:[],gener:[0,1],genuin:[],get:1,get_head:1,get_header_by_nam:1,get_header_index:1,get_rso_byt:1,get_rso_str:1,gethostbynam:[],getpeernam:1,getsocknam:1,getsockopt:1,getter:[],gettimeout:1,github:[],give:[],given:1,global:1,gnu:0,goal:[],going:[],gone:[],got:[],grant:0,gratefulli:0,greater:[],group:1,guid:[],guinea:[],had:[],halt:[],hand:[],handl:1,handle_app_data:[],handle_network_data:[],happen:1,hardwar:[],hardwaretyp:1,has:1,has_head:1,have:1,hdr:[],hdrcl:1,hdrclass:1,hdrname:1,head:[],header:0,hello:[],help:1,here:[0,1],hex:1,highli:[],highlight:[],hijack:[],hold:1,homebrew:[],hop:[],hopcount:1,hope:[],hops_to_root:[],host:1,hostadministrativelyprohibit:1,hostprecedenceviol:1,hostunreach:1,hostunreachableforto:1,how:1,howev:[],html:1,htmlcov:[],http:[0,1],hub:[],hubtest:[],icmp:[],icmpcod:1,icmpcodetimeexceed:1,icmpdata:1,icmpdestinationunreach:1,icmpechorepli:1,icmpechorequest:1,icmpredirect:1,icmpsourcequench:1,icmptimeexceed:1,icmptyp:1,icmptypecodemap:1,icmpv6:1,icmpv6neighboradvertis:1,icmpv6neighborsolicit:1,icmpv6opt:1,icmpv6optionredirectedhead:1,icmpv6optionsourcelinklayeraddress:1,icmpv6optiontargetlinklayeraddress:1,icmpv6redirectmessag:1,icmpv6typ:1,idea:[],identifi:1,idiom:[],idx:1,ieee8023:1,ieee:1,ietf:1,ifnum:1,iftyp:1,ignor:1,illog:[],illustr:[],imaginari:[],immedi:[],implement:1,importantli:[],importerror:[],imposs:[],improv:[],incid:1,includ:[0,1],inclus:[],incom:[],increas:[],incred:[],indefinit:[],index:[0,1],indic:1,individu:1,infer:[],infinit:[],info:1,inform:1,inher:[],initi:1,inout1:[],input:1,input_port:1,insert:1,insert_head:1,inspect:1,instal:0,instanc:1,instanti:1,instead:[],instruct:0,integ:1,integr:[],intend:1,interact:1,interfac:0,interface_by_ipaddr:1,interface_by_macaddr:1,interface_by_nam:1,interface_nam:1,interfacetyp:0,intern:0,internet:0,interoper:[],interpret:[],intf:[],introduc:0,introduct:0,invalid:1,invoc:[],invok:1,involv:[],ip_address:1,ip_ani:1,ip_broadcast:1,ipaddr:1,ipaddress:1,ipid:1,ipinterfac:1,ipprotocol:1,iptabl:[],ipv4:1,ipv4address:1,ipv6:1,ipv6address:1,irrelev:[],is_bridge_filt:1,is_glob:1,is_loc:1,is_multicast:1,isbridgefilt:1,isglob:1,isloc:1,ismulticast:1,isn:1,isol:[],issu:[],item:1,its:1,itself:[],jsommer:[],just:1,keep:[],kei:1,kernel:[],keyerror:[],keyword:1,kind:1,know:[],kwarg:1,lambda:[],laptop:[],last:1,lastli:[],later:[],latter:[],layer:0,lead:[],learn:[],least:[],leav:[],led:[],left:[],len:1,length:1,leon:[],less:[],let:[],level:1,lib:1,libffi:[],libpcap:[],librari:1,light:[],like:0,likewis:[],limit:[],line:0,link:[],linux:[],list:1,listen:1,littl:[],live:[0,1],lldp:1,llnetbas:1,llnettest:[],lo0:[],load:[],local:1,local_addr:1,localaddr:1,localhost:[],localport:1,locat:1,log:1,log_debug:1,log_failur:1,log_info:1,log_warn:1,logic:[],longer:[],longest:[],look:[],lookup:[],loop:[],loopback:1,lot:[],love:[],low:1,lower:[],lowest:[],mac:1,macaddr:1,machin:[],maco:[],made:1,madison:[],magenta:[],magic:[],mai:1,main:1,main_loop:[],maintain:[],major:[],make:1,malform:[],mani:1,manipul:[],map:1,mapdict:1,mask:1,match:1,materi:0,matter:[],mayb:[],mean:[],meaning:[],meant:[],meantim:[],mention:[],messag:[],met:[],method:1,middlebox:[],might:[],minimum:[],mininet:[],minor:[],mirror:[],misnom:1,miss:[],mnemon:1,mode:1,model:1,modif:[],modifi:1,modul:[0,1],more:0,moreov:[],most:1,mostli:[],mother:1,motiv:[],move:[],mpl:1,much:1,multicast:1,multipl:[],must:1,my_interfac:[],myhub:[],mysteri:[],name:1,namedtupl:[],namespac:1,nation:0,natur:[],nearli:[],necessari:[],necessarili:0,need:1,neg:[],net:0,netdata:[],netmask:1,netobj:[],network:[0,1],networkadministrativelyprohibit:1,networkunreach:1,networkunreachableforto:1,next:1,nexthead:1,nexthopmtu:1,nice:[],node:1,nohandl:[],non:1,noncommerci:0,none:1,nopacket:1,nopdb:[],normal:[],notabl:[],note:[0,1],noth:[],notic:1,now:[],noxrepo:[],nsf:0,ntoh:[],ntohl:[],num_head:1,number:1,numer:1,obfusc:[],object:0,observ:[],obsolet:[],obtain:1,occur:1,occurr:[],octet:1,off:[],offset:1,often:[],onc:[],one:1,onli:1,onto:[],oop:[],open:[],openflow:1,oper:[0,1],opinion:0,opt:[],option:[0,1],optnum:1,orchestr:[],order:[],org:[0,1],organ:[],origdgramlen:1,ospf:[],osrg:[],other:1,otherwis:1,oui:1,our:[],out:1,outgo:[],output:[0,1],output_port:1,over:[],overal:[],overrideflag:1,overview:0,overwhelm:[],own:1,pack:1,packag:[],packet:0,packethead:1,packetheaderbas:1,packetinputev:1,packetinputtimeoutev:1,packetio:1,packetoutputev:1,packsiz:[],page:0,pair:[],param:[],paramet:1,pars:0,part:[],partial:[],particular:[0,1],particularli:1,pass:[0,1],path:[],pattern:1,paul:[],paus:[],payload:1,pcapffi:[],pdb:0,pedant:[],pend:[],per:1,perform:[],perhap:[],perspect:1,pfctl:[],physic:[],pictur:[],piec:[],pig:[],pip3:[],pip:[],pkt:1,pktobj:[],place:[],platform:[],plu:[],plural:[],point:[],polici:[],pollut:1,popul:[],popular:[],port:1,port_by_ipaddr:1,port_by_macaddr:1,port_by_nam:1,portion:1,portnam:[],portunreach:1,possibl:1,potenti:[],pox:1,precedencecutoffineffect:1,preconfigur:[],predic:[],prefix:[],prepend_head:1,prerout:[],present:[],pretti:[],prevent:[],previou:[],previous:1,primarili:[],print:1,printf:[],prior:[],privileg:[],probabl:[],problem:1,procedur:[],process:[],prof:[],program:[0,1],progress:[],project:[],prompt:[],proof:[],properli:[],properti:1,prot:[],proto:1,protocol:0,protocolstack:[],protocoltyp:1,protocolunreach:1,prototyp:[],provid:[],psh:1,publicli:[],pudb:[],purpos:[],push:1,put:[],python3:[],python:1,quantiti:1,queri:1,queue:[],quit:[],quot:[],rais:1,rang:1,rare:[],rather:[],raw:1,rawpacketcont:1,rawpackethead:[],read:1,readabl:[],reader:[],real:1,realiz:[],realli:[],reanimated_pkt:[],reason:[],receiv:1,receivedpacket:1,recent:1,recip:0,recogn:[],recommend:0,reconstruct:1,recurs:[],recv:1,recv_from_app:1,recv_into:1,recv_packet:1,recvdata:[],recvfrom:1,recvfrom_into:1,recvmsg:1,red:[],redesign:[],redirect:1,redirected_packet:1,redirectmessag:1,redirectto:1,refer:0,reflect:0,regard:[],regist:[],regular:[],rel:1,relai:1,relat:1,releas:0,relev:[],remain:1,remot:1,remote_addr:1,remoteaddr:1,remoteport:1,remov:1,renam:[],replac:[],repli:1,repo:[],report:[],repositori:[],repr:[],repres:1,represent:1,request:1,requir:1,rerun:[],resembl:[],resort:[],resourc:[],respect:1,respond:[],respons:[],rest:[],restor:[],restrict:[],result:[],retriev:[],returnv:1,reus:[],revis:[],rewrit:[],rfc4861:1,rhello:[],right:[],room:1,root:[],rout:[],router:[0,1],routerflag:1,rst:1,ruan:[],rule:[],run:[0,1],runtim:[],ryu:[],sai:[],same:1,sandwich:[],saul:[],save:[],scenario:0,scienc:0,screen:[],script:[],seamlessli:[],sean:[],search:0,second:1,section:1,see:1,segment:1,self:[],semant:[],send:1,send_packet:1,send_to_app:1,sendal:1,sender:1,senderhwaddr:1,senderprotoaddr:1,sendmsg:1,sendto:1,sens:[],sensibl:[],sent:[],separ:1,seq:1,sequenc:1,seri:[],serial:1,server:[],servic:[],session:[],set:1,set_next_header_class_kei:1,set_next_header_map:1,setblock:1,setsockopt:1,setter:[],settimeout:1,setuptool:[],sever:1,shanabrook:[],share:[],sharealik:0,she:[],sheep:[],shell:[],shift:1,shorthand:[],should:1,shouldn:[],show:[],shown:1,shut:1,shutdown:1,side:[],signal:[],signifi:[],significantli:[],similar:[],similarli:[],simpl:1,simpler:1,simpli:1,simplifi:[],sinc:1,singl:[],situat:[],size:1,slight:1,slightli:[],slow:1,sniff:[],sock_dgram:[],socket:[0,1],socketpair:[],socktyp:1,softwar:0,sole:[],solicitedflag:1,some:1,someth:[],sometim:[],somewhat:[],sourc:1,sourcehostisol:1,sourcequench:1,sourceroutefail:1,space:[],span:[],spanningtreemessag:[],speak:[],special:1,specialipv4addr:1,specialipv6addr:1,specif:[0,1],specifi:[],speed:[],spm:[],spring:[],src:1,srchw:1,srcip:1,srpy:[],stack:[0,1],stand:1,standard:[],start:1,startidx:1,startup:[],state:[],statement:[],step:[],still:[],stop:[],store:1,str:1,straight:[],streamlin:[],strictli:[],string:1,strip:1,struct:[],structur:[],stuck:[],student:[],style:[],subject:[],subnet:1,subsequ:1,subset:[],substitut:[],succe:1,success:[],sudo:[],suffer:[],suggest:[],sum:[],summari:[],superus:[],suppli:[],support:[0,1],sure:[],surpris:[],surprisingli:[],switchi:1,switchy_main:[],switchyard:1,switchyardtestev:[],swyard:[],syenv:[],symbol:1,syn:1,syntax:[],system:0,tabl:[],tack:1,tag:[],take:1,target:[],targetaddr:1,targethwaddr:1,targetip:1,targetprotoaddr:1,task:[],tcp:[],tell:[],term:0,termin:[],test:0,testmod:1,testscenario2:[],testscenario:1,text:1,than:[],thank:0,thei:1,them:1,thi:[0,1],thing:[],think:[],those:0,though:[],thread:[],threadsaf:[],three:1,through:1,thu:[],time:[],timeexceed:1,timeout:1,timestamp:1,to_byt:1,togeth:[],token:[],too:1,tool:1,top:[],topic:0,toraw:1,tos:1,tostr:1,total_length:1,totupl:1,trace:[],traceback:1,track:[],tradition:[],traffic:[],trafficclass:1,transport:[],trap:[],tree:[],troubl:[],truncat:[],ttl:1,ttlexpir:1,tupl:1,turn:[],twice:[],two:1,txt:[],type:[0,1],typic:1,udp:[],udp_ping_port:[],udpstack:[],udpstack_test:[],unbound:[],uncompil:[],undefin:1,under:0,underli:[],understand:[],understood:[],undesir:[],undocu:1,unexpect:[],uniqu:1,univers:[],unix:[],unknown:1,unless:1,unmodifi:[],unpack:[],unsign:[],until:[],unus:[],up1:[],up2:[],up3:[],upon:0,urg:1,urgent_point:1,usag:[],use:1,used:1,useful:1,user:[],userlib:1,uses:1,using:1,usr:[],utf8:[],util:0,valid:1,validli:1,valu:1,valueerror:1,variabl:[],varieti:[],variou:1,venv:[],verbos:0,veri:[],verifi:1,version:0,via:[],view:0,virtual:[],virtualenv:[],visual:[],vlan:[],vlanid:[],wai:[],wait:[],walk:[],want:1,warn:1,well:1,were:[],weren:[],what:1,when:[0,1],whenev:[],where:1,wherea:[],whether:1,which:1,who:[],why:[],wildcard:[],wilson:[],window:1,wire:1,wireless:1,wisconsin:[],wise:[],wish:[],within:1,without:[],wooli:[],work:0,workaround:[],world:[],worth:[],would:1,wrap:1,wrapper:1,write:0,written:[],wrong:[],www:[],x00:1,x00e:[],x01:1,x02:[],x03:[],x08:[],x0c:[],x11:[],x14:1,x17:[],x8021ad:1,x8021ah:1,x8021q:1,x84:[],x88:[],x9d:[],x9e:[],xad8g:[],xb1:[],xb4:[],xb7:[],xba:[],xbyte:[],xc3:[],xc5:[],xca5k:[],xd1l:[],xd6:[],xeap:[],xec:[],xech:[],xf0:[],xfb:[],xhop:[],xhub:[],xroot:[],xterm:[],xuyi:[],yang:[],yield:[],you:[0,1],your:1,yourcod:[],yourself:[],yum:[],zero:1},titles:["Switchyard documentation","API Reference"],titleterms:{"class":1,"function":1,"new":[],One:[],about:[],acknowledg:[],address:1,advanc:[],anoth:[],api:1,applic:1,argument:[],arp:1,basic:[],call:[],check:[],code:[],command:[],compil:[],configur:[],construct:1,control:1,coverag:[],creat:[],creation:1,datagram:1,debug:[],debugg:[],deliv:[],devic:[],document:0,don:[],emul:[],environ:[],ethernet:1,even:[],exampl:[],exclud:[],fail:[],fedora:[],firewal:[],from:[],full:[],get:[],header:1,icmp:1,includ:[],indic:0,inform:[],instal:[],instruct:[],interfac:1,interfacetyp:1,internet:1,introduc:[],introduct:[],invok:[],layer:1,librari:[],licens:0,like:[],line:[],live:[],log:[],lower:[],maco:[],messag:1,method:[],more:[],net:1,network:[],note:[],object:1,oper:[],option:[],other:[],output:[],overview:[],packet:1,pars:1,particular:[],pass:[],pdb:[],port:[],program:[],protocol:1,receiv:[],recip:[],redhat:[],refer:1,releas:[],resolut:1,run:[],scenario:1,send:[],socket:[],specif:[],stack:[],start:[],switchyard:0,swyard:[],system:[],tabl:0,tcp:1,test:1,thank:[],topic:[],transmiss:1,type:[],ubuntu:[],udp:1,user:1,util:1,verbos:[],version:1,when:[],write:[],you:[]}})