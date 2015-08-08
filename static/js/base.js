// JavaScript Document
//主页布局模块公共
$.fn.extend({
    pageWrap:function(options){
        var defaults={
            side:".side",
            main:".main",
        }
        var options= $.extend(defaults,options);
        this.each(function(){
            var That=$(this);
            var Mantle={
                oSide:That.find(options.side),
                oMain:That.find(options.main),
                oModW:300,
                init:function(){
                    this.Position();
                },
                Position:function(){
                    var docmenuW=$(document).width()+$(window).scrollLeft();
                    var docmenuH=$(document).height()+$(window).scrollTop();
                    var pageW=$(window).width()+$(window).scrollLeft();
                    var pageH=$(window).height()+$(window).scrollTop();
                    if(pageW<600){pageW=600}
                    if(pageH<400){pageH=400}
                    pageH<=docmenuH?docmenuH:pageH;
                    if(pageH<=this.oMain.height()){pageH=this.oMain.height()}
                    this.oSide.css({"height":pageH});
                    this.oMain.css({"width":pageW-this.oSide.outerWidth(),"height":pageH});
                    this.oMain.find(".mod").css({"width":this.oMain.outerWidth(),"height":pageH});
                    $(".popbg").css({"width":pageW,"height":pageH});
                },
            }
            Mantle.init();
            $(window).bind("resize",function(){
                Mantle.init();
            })  
        })
    }
})  

//左侧导航
$.fn.extend({
    sideNav:function(options){
        var defaults={
            sideNav:"#nav",
            subNav:".subnav"        
        }
        var options= $.extend(defaults,options);
        this.each(function(){
            var That=$(this);
            var Mantle={
                oNav:That,
                oNavLi:That.children(),
                oSubnav:That.find(options.subNav),  
                init:function(){
                    this.oSubnav.eq(options.index).css("height",this.oSubnav.eq(options.index).find("li").eq(options.index).height()*this.oSubnav.eq(options.index).children().length);
                    this.oNavLi.eq(options.index).addClass("on");
                    this.clickfn();
                },
                clickfn:function(){
                    var This = this;
                    This.oNavLi.bind("click",function(event){
                        This.oNavLi.removeClass("on");
                        This.oSubnav.stop().animate({height:0},"slow"); 
                        var subnavH=This.oSubnav.eq(0).find("li").eq(0).height()*$(this).find("ul").children().length;
                        if($(this).find("ul").height()==0){
                            $(this).addClass("on");
                            $(this).find("ul").stop().animate({height:subnavH},"slow"); 
                        }
                        else{
                            $(this).find("ul").stop().animate({height:0},"slow");   
                        }
                    })  
                    This.oSubnav.click(function(event){
                        event.stopPropagation();
                    })
                }       
            }
            Mantle.init();  
        })
    }    
})  

//点击请假／提醒
$.fn.extend({
    setState:function(options){
        var defaults={
            oState:".state",
            oSpan:"span",
            oEm:"em",
            arr:{a:"已请假",b:"已提醒"}
        }
        
        var options= $.extend(defaults,options);
        this.each(function(){
            var That=$(this);
            var Mantle={
                oState:That.find(options.oState),
                oSpan:That.find(options.oSpan),
                oEm:That.find(options.oEm),
                arr:options.arr,
                init:function(){
                    this.clickfn();
                },
                clickfn:function(){
                    var _This=this;
                    _This.oEm.bind("click",function(){
                        var This=$(this);
                        $(".tips").remove();
                        This.after(_This.creatTips());
                        $(".tips").css("display","block");
                        $(".tips").find("li").click(function(){ 
                            if($(this).index()==0){
                                This.prev().attr("class","green").html(_This.arr.a)
                            }
                            if($(this).index()==1){
                                This.prev().attr("class","blue").html(_This.arr.b)
                            }
                        })
                
                        $(document).click(function(){
                            $(".tips").remove();
                        })
                        return false;
                    })
                },
                creatTips:function(){
                    var $tips=$("<div class='tips'></div>")
                    var $ul = $('<ul></ul>');
                    var $li1 = $('<li><span><a href="#">'+'已请假'+'</a></span></li>');
                    var $li2 = $('<li><span><a href="#">'+'邮件提醒'+'</a></span></li>');
                    $li1.appendTo($ul);
                    $li2.appendTo($ul);
                    $ul.appendTo($tips);
                    return $tips;
                }
            }
            
            Mantle.init();  
        })
    }
})

//汇总页滚动条
$.fn.extend({
    dropDown:function(options){
        var parameter = {
            contBox:'.txt',
            dorpBox:'.drap',
            Drop:'em',
        }
        var options = $.extend(parameter,options);
        this.each(function(){
            var That = $(this);
            var DropDown = {
                init:function(){
                    this.dropDowmBox = That;
                    this.options = options;
                    this.contBox = this.dropDowmBox.find(options.contBox);
                    this.dorpBox = this.dropDowmBox.find(options.dorpBox);
                    this.Drop = this.dropDowmBox.find(options.Drop);
                    this.scale = 0;
                    this.height = 0;
                    this.maxTop = 0;
                    this.listMaxTop = 0;
                    this.t = 0;

                    this.scale = this.dropDowmBox.height()/(this.contBox.height()-10);
                    
                    if(this.scale>=1){
                        this.dorpBox.hide();
                    }
                    else{
                        this.dorpBox.show()

                        this.dorpBox.css("height",this.dropDowmBox.height())
                        this.height = this.dorpBox.height()*this.scale;         
                        this.Drop.css({'height':this.height});
                        this.maxTop = this.dorpBox.height() - this.height;
                        this.listMaxTop = this.contBox.outerHeight(true)- this.dropDowmBox.height();
    
                        this.DropMove();
                        this.MouseScroll();
                        this.clickScroll();
                    }
                },
                DropMove:function(){
                    var oDrop = this.Drop
                    var That = this;
                    oDrop.mousedown(function(e){
                        var disY = e.pageY -$(this).get(0).offsetTop;
                        $(document).mousemove(function(e){
                            That.t = e.pageY-disY;
                            That.MoveScrop();
                        });
                        $(document).mouseup(function(){
                            $(document).off();
                        })
                        return false;
                    });
                },
                MoveScrop:function(){
                    if(this.t<0){
                        this.t = 0;
                    }else if(this.t>this.maxTop){
                        this.t = this.maxTop;
                    }
                    
                    this.contBox.css('top',-this.t*this.listMaxTop/this.maxTop);
                    this.Drop.css('top',this.t);
                    return false;
                },
                MouseScroll:function(){
                    var oBox = this.dropDowmBox.get(0);
                    var That = this;
                    oBox.onmousewheel = WheelTop;
                    if(oBox.addEventListener){
                        oBox.addEventListener('DOMMouseScroll',WheelTop,false)
                    }
                    function WheelTop(ev){
                        var e = ev || event;
                        var fe = e.wheelDelta||e.detail;
                        var bDown = true;
                        
                        if(e.detail){
                            bDown = fe>0?true:false;
                        }
                        else{
                            bDown = fe>0?false:true;
                        }
                        if(bDown){
                            That.t+=10
                        }else{
                            That.t-=10
                        }
                        That.MoveScrop();
                        
                        if(e.preventDefault){
                            e.preventDefault();
                        }
                        return false;
                    }
                },
                clickScroll:function(e){
                    var That = this;
                    this.dorpBox.click(function(e){
                        var dir = e.pageY-That.Drop.offset().top;
                        if(dir>0){
                            That.t+=10
                        }else{
                            That.t-=10
                        }
                        That.MoveScrop();
                        return false;
                    });
                    That.Drop.click(function(){
                        return false;
                    })
                }
            }
            DropDown.init();
            $(window).bind("resize",function(){
                DropDown.init();
            })  
        })
    }
})

//汇总页点击切换
function dropDownClick(obj){
    var oSummary=$(obj);
    var oTit=oSummary.find(".tit");
    var oCont=oSummary.find(".cont");   
    var oDt=oSummary.find("dt");
    var oDD=oSummary.find("dd");    
    if(oTit.length!=0){
        oTit.click(function(){
            if($(this).next().height()!=0){
                $(this).next().stop().animate({height:0},"slow")    
            }
            else{
                $(this).next().stop().animate({height:$(this).next().find("dl").outerHeight()*$(this).next().find("dl").length-$(this).next().find("dl").length},"slow");   
            }
        })
    }
    else{
        oDt.click(function(){   
            if($(this).next().height()!=0){
                $(this).next().stop().animate({height:0},"slow")    
            }
            else{
                $(this).next().stop().animate({height:$(this).next().find("ul").height()-1},"slow");    
            }
        })
    }
}

//弹出层   
$.fn.extend({
    popBox:function(options){
        var defaults={
            oPop:".addteam",
            oTitMove:".title",
            oClose:"span",
            oBtn:".add",
            giveup:{div:"giveup",txt:"放弃修改内容？",onoff:false},
            detail:{onoff:false},
        }
        
        var options= $.extend(defaults,options);
        this.each(function(){
            var That=$(this);
            var Mantle={
                oPop:That,
                oTitMove:That.find(options.oTitMove),
                oClose:That.find(options.oTitMove).find(options.oClose),
                oBtn:$(options.oBtn),
                oAddSub:That.find(".addsub"),
                oGiveup:options.giveup,
                oDetail:options.detail,
                
                init:function(){
                    this.btnClick();
                    this.closeClick();
                    this.Position();
                    this.oStartMove();
                    this.addSub();
                },
                btnClick:function(){
                    var That = this;
                    That.oBtn.bind("click",function(){
                        That.oPop.css("display","block");
                        $(".popbg").css({"display":"block"});
                        if(That.oBtn.parents(".modpop")!=null){
                            That.oBtn.parents(".modpop").css("display","none");
                        }
                        That.Position();
                    })
                },
                creatGiveup:function(){
                    var That=this;
                    var $giveup=$("<div class='giveup' id="+That.oGiveup.div+"></div>");
                    var $giveupTxt = $("<p>"+That.oGiveup.txt+"</p>");
                    var $giveupBtn = $("<div class='btn'><a href='javascript:;'>确定</a><a href='javascript:;'>取消</a></div>");
                    $giveupTxt.appendTo($giveup);
                    $giveupBtn.appendTo($giveup);
                    return $giveup
                },
                closeClick:function(){
                    var That = this;
                    That.oClose.bind("click",function(){
                        if(!That.oGiveup.onoff){
                            $(".popbg").css({"z-index":"100"});
                            That.creatGiveup().appendTo($(document.body));
                            $("#"+That.oGiveup.div).css({top:$(window).height()/2-$(".giveup").outerHeight()/2+$(window).scrollTop(),left:$(window).width()/2-$(".giveup").outerWidth()/2+$(window).scrollLeft()});
                            $("#"+That.oGiveup.div).find(".btn").find("a").eq(0).click(function(){
                                $("#"+That.oGiveup.div).remove();
                                That.oPop.css("display","none");
                                $(".popbg").css({"z-index":"98","display":"none"});
                            })
                            $("#"+That.oGiveup.div).find(".btn").find("a").eq(1).click(function(){
                                $("#"+That.oGiveup.div).remove();
                                $(".popbg").css({"z-index":"98"});
                            })
                        }
                        if(That.oDetail.onoff){
                            That.oPop.css("display","none");
                            $(".popbg").css({"z-index":"98","display":"none"}); 
                        }
                    })
                },
                Position:function(){
                    var iw=$(window).width()/2-this.oPop.width()/2+$(window).scrollLeft();
                    var ih=$(window).height()/2-this.oPop.height()/2+$(window).scrollTop();
                    
                    if(ih<=0){ih=0};
                    this.oPop.css({top:ih,left:iw})
                    $("#"+this.oGiveup.div).css({top:$(window).height()/2-$(".giveup").outerHeight()/2+$(window).scrollTop(),left:$(window).width()/2-$(".giveup").outerWidth()/2+$(window).scrollLeft()});
                },
                oStartMove:function(){
                    var That = this;
                    That.oTitMove.bind("mousedown",function(e){ 
                        var ih=That.oPop.offset().top;
                        var iw=That.oPop.offset().left;
                        var disY = e.pageY -$(this).get(0).offsetTop;
                        var disX = e.pageX -$(this).get(0).offsetLeft;
                        
                        var pageW=$(window).width()+$(window).scrollLeft();
                        var pageH=$(window).height()+$(window).scrollTop();
                        var oMain=$(".main")
                        if(pageH<=oMain.height()){pageH=oMain.height()}
                        
                        $(document).mousemove(function(e){
                            var T= e.pageY-disY+ih;
                            var L= e.pageX-disX+iw;
                            if(T<=0){
                                T=0;
                            }
                            if(T>=pageH-That.oPop.height()){
                                T=pageH-That.oPop.height();
                            }
                            if(L<=0){
                                L=0;    
                            }
                            if(L>=$(window).width()-That.oPop.width()){
                                L=$(window).width()-That.oPop.width();
                            }
                            
                            That.oPop.css({top:T,left:L})
                        });
                        
                        $(document).mouseup(function(){
                            $(document).off();
                        })
                        return false;
                    })  
                },

                addSub:function(){
                    var That=this;
                    That.oAddSub.find("dt").find("em").click(function(){
                        var $dd=$("<dd></dd>")
                        var $span0 = $("<span>角色</span><div class='select'><p class='add_role'>组员</p><ul><li><a href='javascript:;'>组员</a></li><li><a href='javascript:;'>观察者</a></li></ul></div>");
                        var $span1 = $("<span>邮箱</span><input name='' type='text' class='addsub_email' style='color: rgb(0, 0, 0);'/>");
                        var $span2 = $("<span>姓名</span><input name='' type='text' class='addsub_username' style='color: rgb(0, 0, 0);'/>");
                        var $em = $("<em><img src='/static/images/minus.png' title='删除'></em>");
                        $span0.appendTo($dd);
                        $span1.appendTo($dd);
                        $span2.appendTo($dd);
                        $em.appendTo($dd);
                        $dd.appendTo(That.oAddSub);
                        //当前team做设置管理--模似select下框列表框
                        $(".select").Select({
                            oSelect:".select",
                            oP:"p",
                            oUl:"ul"
                        });
                        $em.click(function(){
                            $(this).parent().remove();
                        })
                    })
                    That.oAddSub.find("dd").find("em").click(function(){
                        $(this).parent().remove();
                    })
                }
            }
            
            Mantle.init();
            $(window).bind("resize",function(){
                Mantle.Position();
            })  
            
        })
    }    
})

//模似select下框列表框
$.fn.extend({
    Select:function(options){
        var defaults={
            oSelect:".select",
            oP:"p",
            oUl:"ul",
        }
        
        var options= $.extend(defaults,options);
        this.each(function(){
            var That=$(this);
            var Mantle={
                oSelect:That,
                oP:That.find(options.oP),
                oUl:That.find(options.oUl),
                init:function(){
                    this.clickfn();
                },
                clickfn:function(){
                    var _This=this;
                    _This.oP.bind("click",function(){
                        var This=$(this);
                        $(options.oSelect).find(options.oUl).css("display","none");
                        _This.oUl.css("display","block");
                        _This.oUl.find("li").click(function(){
                            _This.oP.html($(this).text())
                            
                        })
                        
                        $(document).click(function(){
                        $(options.oSelect).find(options.oUl).css("display","none");
                        //$(document).off();
                        })
                        return false;
                    })
                    
                },
            }            
            Mantle.init();  
        })
    }
})

//日报、周报切换
$.fn.extend({
    dayWeekly:function(){
        var defaults={
            oPop:".setteam",
            oType:".type",
            oDay:".day",
            oWeek:".week",
        }
        var options= $.extend(defaults,options);
        this.each(function(){
            var That=$(this);
            var Mantle={
                oPop:That,
                oType:That.find(options.oType),
                oDay:That.find(options.oDay),
                oWeek:That.find(options.oWeek),
                init:function(){
                    this.clickfn()
                },
                clickfn:function(){
                    var That=this;
                    That.oType.find("li").click(function(){
                        That.oType.find("li").removeClass("cur");
                        $(this).addClass("cur");
                        if($(this).index()==0){
                            That.oWeek.css("display","none");
                            That.oDay.css("display","block");
                        }
                        if($(this).index()==1){
                            That.oDay.css("display","none");
                            That.oWeek.css("display","block");
                        }
                    })
                },
            }
            Mantle.init();
        })
    }   
})

//团队成员删除    
$.fn.extend({
    Members:function(options){
        var defaults={
            oMembers:".members",
            oLi:"li",
            giveup:{div:"giveup",txt:"确定将1由2中移除？"},
        }
        var options= $.extend(defaults,options);
        this.each(function(){
            var That=$(this);
            var Mantle={
                oMembers:That,
                oLi:That.find(options.oLi),
                oGiveup:options.giveup,
                
                init:function(){
                    this.obClick();
                },
                
                creatGiveup:function(){
                    var _this=this;
                    var $giveup=$("<div class='giveup' id="+_this.oGiveup.div+"></div>");
                    var $giveupTxt = $("<p>"+_this.oGiveup.txt+"</p>");
                    var $giveupBtn = $("<div class='btn'><a href='javascript:;'>确定</a><a href='javascript:;'>取消</a></div>");
                    $giveupTxt.appendTo($giveup);
                    $giveupBtn.appendTo($giveup);
                    return $giveup
                },
                obClick:function(){
                    var _this = this;
                    _this.oLi.find("b").bind("click",function(){
                        var _This=$(this);
                        _this.oLi.find("b").removeClass("cur");
                        _This.addClass("cur");
                        $(".popbg").css({"z-index":"100","display":"block"});
                        _this.creatGiveup().appendTo($(document.body));
                        $("#"+_this.oGiveup.div).css({top:$(window).height()/2-$(".giveup").outerHeight()/2+$(window).scrollTop(),left:$(window).width()/2-$(".giveup").outerWidth()/2+$(window).scrollLeft()});
                        
                        $("#"+_this.oGiveup.div).find(".btn").find("a").eq(0).click(function(){
                            $("#"+_this.oGiveup.div).remove();
                            _This.parent("li").remove();
                            $(".popbg").css({"z-index":"98","display":"none"});
                        })
                        $("#"+_this.oGiveup.div).find(".btn").find("a").eq(1).click(function(){
                            $("#"+_this.oGiveup.div).remove();
                            $(".popbg").css({"z-index":"98","display":"none"});
                            _this.oLi.find("b").removeClass("cur");
                        })
                    })
                },
                Position:function(){
                    $("#"+this.oGiveup.div).css({top:$(window).height()/2-$(".giveup").outerHeight()/2+$(window).scrollTop(),left:$(window).width()/2-$(".giveup").outerWidth()/2+$(window).scrollLeft()});
                },
                
            }
            
            Mantle.init();
            $(window).bind("resize",function(){
                Mantle.Position();
            })  
        })
    }    
})

//进度条   
$.fn.extend({
    Progress:function(options){
        var defaults={
            oProgress:".progress",
            oBar:".bar",
            oRate:".rate",
            oPre:".pre",
        }
        
        var options= $.extend(defaults,options);
        this.each(function(){
            var That=$(this);
            var Mantle={
                oProgress:That,
                oBar:That.find(options.oBar),
                oRate:That.find(options.oRate),
                oPre:That.find(options.oPre),
                init:function(){
                    this.preMove();
                },
                preMove:function(){
                    var _That = this;
                    _That.oPre.css("left",parseInt(_That.oPre.text())/100*162)
                    _That.oPre.text(parseInt(_That.oPre.text())+"%")
                    _That.oRate.css("width",parseInt(_That.oPre.text())/100*180)
                    _That.oPre.bind("mousedown",function(e){
                        var iw=_That.oPre.position().left;
                        var disX = e.pageX;
                        $(document).mousemove(function(e){
                            var L= e.pageX-disX+iw;
                            if(L<=0){
                                L=0;
                            }
                            if(L>=_That.oBar.width()-_That.oPre.width()){
                                L=_That.oBar.width()-_That.oPre.width();
                            }
                            _That.oPre.text(Math.ceil(L/162*100)+"%")
                            _That.oRate.css("width",Math.ceil(L/162*100)+"%")
                            _That.oPre.css({left:L})
                        });
                        
                        $(document).mouseup(function(){
                            $(document).off();
                        })
                        return false;
                        
                    })
                    
                },
            }
            Mantle.init();
        })
    }   
})

//下拉列表切换状态
function switchState(obj){
    var oSwitch=$(obj);
    var oSwitchLi=oSwitch.find("li");
    oSwitchLi.click(function(){ 
        $(".progress").css("display","none");  
        $(".status_change_select").css("display","none");   
        if($(this).index()==0){
            $(obj).attr("class","switch nostart")       
        }
        if($(this).index()==1){
            $(obj).attr("class","switch doing");
            $(".progress").css("display","block");
            $(".status_change_select").css("display","block");
            $(".real_time_start_done_class").html("开始时间:");
        }
        if($(this).index()==2){
            $(obj).attr("class","switch finish");
            $(".progress").css("display","block"); 
            $(".status_change_select").css("display","block");
            $(".real_time_start_done_class").html("完成时间:");
        }
        if($(this).index()==3){
            $(obj).attr("class","switch delay");    
        }
    })
}
//input获得焦点
$.fn.extend({
    oInput:function(){
        var defaults={
            oInput:"input",
        }
        var options= $.extend(defaults,options);
        this.each(function(){
            var That=$(this);
            var Mantle={
                oInput:That,
                init:function(){
                    this.clickfn()
                },
                clickfn:function(){
                    var That=this;
                    var state=false;
                    var oTxt=null;
                    if(That.oInput.attr("class")=="nofocus"){
                        state=true;
                    }
                    else{
                        state=false;
                    }
                    That.oInput.bind("focus",function(){
                        if(!state){
                            oTxt=$(this).val();
                            state=true;
                        }
                        if($(this).val()==oTxt){
                            $(this).val("");
                            $(this).css("color","#000000");
                        }
                        $(this).blur(function(){
                            if($(this).val()==""){
                                $(this).val(oTxt);
                                $(this).css("color","#b3b7c1");
                            }   
                        })
                    })
                },
            }
            Mantle.init();
        })
    }   
})

//input获得焦点
$.fn.extend({
    oInput:function(){
        var defaults={
            oInput:"input",
        }
        var options= $.extend(defaults,options);
        this.each(function(){
            var That=$(this);
            var Mantle={
                oInput:That,
                init:function(){
                    this.clickfn()
                },
                clickfn:function(){
                    var That=this;
                    var state=false;
                    var oTxt=null;
                    if(That.oInput.attr("class")=="nofocus" || That.oInput.attr("class")=="yet"){
                        That.oInput.css("color","#000000");
                        state=true;
                    }
                    else{
                        state=false;
                    }
                    That.oInput.bind("focus",function(){
                        if(!state){
                            oTxt=$(this).val();
                            state=true;
                        }
                        if(!state){
                            oTxt=$(this).val();
                            state=true;
                        }
                        if($(this).val()==oTxt){
                            $(this).val("");
                            $(this).css("color","#000000");
                        }
                        $(this).blur(function(){
                            if($(this).val()==""){
                                if ($(this).attr('class') == "yet")
                                {
                                    $(this).css("color","#000000");
                                }else{
                                    $(this).val(oTxt);
                                    $(this).css("color","#b3b7c1");
                                }
                            }   
                        })
                    })
                },
            }
            Mantle.init();
        })
    }   
})

//退出系统
function Exit(obj){
    var oBtn=$(obj)
    var stat=false;
    oBtn.click(function(){
        $(".exit").css("display","block");
        var $giveup=$("<div class='giveup' id='exitgiveup'></div>");
        var $giveupTxt = $("<p>确定退出系统？</p>");
        var $giveupBtn = $("<div class='btn'><a href='javascript:;'>确定</a><a href='javascript:;'>取消</a></div>");
        $giveupTxt.appendTo($giveup);
        $giveupBtn.appendTo($giveup);
        $(".exit").click(function(){ 
            if(!stat){
                $giveup.appendTo($(document.body));
                 stat=true;
            }
            $(".popbg").css({"z-index":"100","display":"block"});
            $("#exitgiveup").css({top:$(window).height()/2-$(".giveup").outerHeight()/2+$(window).scrollTop(),left:$(window).width()/2-$(".giveup").outerWidth()/2+$(window).scrollLeft()});
            $("#exitgiveup").find(".btn").find("a").eq(0).click(function(){
                $("#exitgiveup").remove();
                location.href ="/logout"
                $(".popbg").css({"z-index":"98","display":"none"});
                stat=false;
            })
            $("#exitgiveup").find(".btn").find("a").eq(1).click(function(){
                $("#exitgiveup").remove();
                $(".exit").css("display","none");
                $(".popbg").css({"z-index":"98","display":"none"});
                stat=false;
            })  
        })
        $(document).click(function(){
            $(".exit").css("display","none");
        })
        return false;
    })      
}


//加载后执行
$(function(){
     try {
    //主页布局
    $(".wrap").pageWrap({
        side:".side",
        main:".main",
    });
    
    //点击请假／提醒
    $(".state").setState({
        oState:".state",
        oSpan:"span",
        oEm:"em",
        arr:{a:"已请假",b:"已提醒"}
    });
    
    //汇总页滚动条
    $('.depict').dropDown({
        contBox:'.txt',  //内容class
        dorpBox:'.drap', //滚动条class
        Drop:'em'      //滚动条的块class
    });
    //汇总页点击切换
    dropDownClick(".summary");

    //当前team做设置管理
    $(".setteam").popBox({
        oPop:"setteam",
        oTitMove:".title",
        oClose:"span",
        oBtn:".set",
        giveup:{div:"setgiveup",txt:"放弃修改内容？"}
    });
    
    //当前team做设置管理--日报、周报切换
    $(".setteam").dayWeekly({
        oPop:".setteam",
        oType:".type",
        oDay:".day",
        oWeek:".week",
    });
    
    //新建team-基本信息第一步
    $(".build1").popBox({
        oPop:"build1",
        oTitMove:".title",
        oClose:"span",
        oBtn:".newteam",
        giveup:{div:"giveup1",txt:"确定放弃新建组群？"}
    });
    
    //新建team-团队成员第二步
    $(".build2").popBox({
        oPop:"build2",
        oTitMove:".title",
        oClose:"span",
        oBtn:".buildbtn2",
        giveup:{div:"giveup2",txt:"确定放弃新建组群？"}
    });
    
    //新建team-团队成员第二步
    $(".build1").popBox({
        oPop:"build1",
        oTitMove:".title",
        oClose:"span",
        oBtn:".buildbtn1",
        giveup:{div:"giveup1",txt:"确定放弃新建组群？",onoff:true}
    });
    
    //新建team-日报、周报设置第三步
    $(".build3").popBox({
        oPop:"build3",
        oTitMove:".title",
        oClose:"span",
        oBtn:".buildbtn3",
        giveup:{div:"giveup3",txt:"确定放弃新建组群？"}
    });
    
    //新建team-任务设置第四步
    $(".build4").popBox({
        oPop:"build4",
        oTitMove:".title",
        oClose:"span",
        oBtn:".buildbtn4",
        giveup:{div:"giveup4",txt:"确定放弃新建组群？"}
    });

    //新建team-日报、周报设置第三步-日报、周报切换
    $(".build3").dayWeekly({
        oPop:".build3",
        oType:".type",
        oDay:".day",
        oWeek:".week",
    });
    
    //当前team做设置管理--模似select下框列表框
    $(".select").Select({
        oSelect:".select",
        oP:"p",
        oUl:"ul"
    });
    
    //任务设置
    $(".taskset").popBox({
        oPop:"taskset",
        oTitMove:".title",
        oClose:"span",
        oBtn:".set",
        giveup:{div:"setgiveup",txt:"放弃修改内容？"}
    });
    
    //新建任务
    $(".newtask").popBox({
        oPop:"newtask",
        oTitMove:".title",
        oClose:"span",
        oBtn:".add",
        giveup:{div:"taskgiveup",txt:"放弃新建任务？"}
    });

    $(".statistics_kpi_pop").popBox({
        oPop:"newtask",
        oTitMove:".title",
        oClose:"span",
        oBtn:".statistics",
        giveup:{div:"taskgiveup",txt:"放弃生成统计信息?"}
    });
    
    //添加团队成员
    $(".addpeople").popBox({
        oPop:"addpeople",
        oTitMove:".title",
        oClose:"span",
        oBtn:".plus",
        giveup:{div:"addgiveup",txt:"放弃添加成员？"}
    });
    
    //进度条
    $(".progress").Progress({
        oProgress:".progress",
        oBar:".bar",
        oRate:".rate",
        oPre:".pre",
    });
    
    //切换状态--模似select下框列表框
    $(".switch").Select({
        oSelect:".switch",
        oP:"p",
        oUl:"ul"
    });
    switchState(".switch")
    
    //input获得焦点
    $("input").oInput({
        oInput:"input",
    }); 
    //textarea获得焦点
    $("textarea").oInput({
        oInput:"textarea",
    }); 
    
    //退出系统
    Exit(".side .user em");
    Exit(".noteam .user em");
    
    
    //新建Team时间控件
    $('#datetimepicker1').datetimepicker({
        datepicker:false,
        format:'H:i',
        step:5
    });
    $('#datetimepicker2').datetimepicker({
        datepicker:false,
        format:'H:i',
        step:5
    });
    $('#datetimepicker3').datetimepicker({
        datepicker:false,
        format:'H:i',
        step:5
    });
    $('#datetimepicker4').datetimepicker({
        datepicker:false,
        format:'H:i',
        step:5
    });
    $('#datetimepicker5').datetimepicker({
        datepicker:false,
        format:'H:i',
        step:5
    });
    $('#datetimepicker6').datetimepicker({
        datepicker:false,
        format:'H:i',
        step:5
    });
    $('#datetimepicker7').datetimepicker({
        datepicker:false,
        format:'H:i',
        step:5
    });
    $(".cur_class_change").click(function(){
        $(this).parent().children().removeClass("cur");
        $(this).addClass("cur");
    });
     } catch (error) {
        console.log(error);
    }
})
    
