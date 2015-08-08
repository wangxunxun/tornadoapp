
_ESCAPEABLE = /["\\\x00-\x1f\x7f-\x9f]/g;
_META = {
        '\b': '\\b',
        '\t': '\\t',
        '\n': '\\n',
        '\f': '\\f',
        '\r': '\\r',
        '"' : '\\"',
        '\\': '\\\\'
};
function eval_json(src){return eval("(" + src + ")");};
js_quote = function(string){
        if (string.match(_ESCAPEABLE))
        {
            return '"' + string.replace(_ESCAPEABLE, function (a)
            {
                var c = _META[a];
                if (typeof c === 'string') return c;
                c = a.charCodeAt();
                return '\\u00' + Math.floor(c / 16).toString(16) + (c % 16).toString(16);
            }) + '"';
        }
        return '"' + string + '"';
};
   

function dump_json(o){
    var type = typeof(o);

    if (o === null)
        return "null";

    if (type == "undefined")
        return undefined;

    if (type == "number" || type == "boolean")
        return o + "";

    if (type == "string")
        return js_quote(o);

    if (type == 'object')
    {
        if (typeof o.toJSON == "function")
            return dump_json( o.toJSON() );

        if (o.constructor === Date)
        {
            var month = o.getUTCMonth() + 1;
            if (month < 10) month = '0' + month;

            var day = o.getUTCDate();
            if (day < 10) day = '0' + day;

            var year = o.getUTCFullYear();

            var hours = o.getUTCHours();
            if (hours < 10) hours = '0' + hours;

            var minutes = o.getUTCMinutes();
            if (minutes < 10) minutes = '0' + minutes;

            var seconds = o.getUTCSeconds();
            if (seconds < 10) seconds = '0' + seconds;

            var milli = o.getUTCMilliseconds();
            if (milli < 100) milli = '0' + milli;
            if (milli < 10) milli = '0' + milli;

            return '"' + year + '-' + month + '-' + day + 'T' +
                hours + ':' + minutes + ':' + seconds +
                '.' + milli + 'Z"';
        }

        if (o.constructor === Array)
        {
            var ret = [];
            for (var i = 0; i < o.length; i++)
                ret.push( dump_json(o[i]) || "null" );

            return "[" + ret.join(",") + "]";
        }

        var pairs = [];
        for (var k in o) {
            var name;
            var type = typeof k;

            if (type == "number")
                name = '"' + k + '"';
            else if (type == "string")
                name = js_quote(k);
            else
                continue;

            if (typeof o[k] == "function")
                continue;

            var val = dump_json(o[k]);

            pairs.push(name + ":" + val);
        }

        return "{" + pairs.join(", ") + "}";
    }
};

function get_r_week(s){
    if(s=="周一"){
        return "1";
    }
    else if(s=="周二"){
        return "2";
    }
    else if(s=="周三"){
        return "3";
    }
    else if(s=="周四"){
        return "4";
    }
    else if(s=="周五"){
        return "5";
    }
    else if(s=="周六"){
        return "6";
    }
    else if(s=="周日"){
        return "7";
    }
    else{
        return "5";
    }
}

function isEmail(str){
       var reg = /^([a-zA-Z0-9_.-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/;
       return reg.test(str);
}

function check_day_week(day_detail_create_time, day_detail_summary_time, week_detail_create_time, week_detail_summary_time, day_detail_remind_interval, week_detail_remind_interval)
{
    if(day_detail_create_time){
            
    }else{
        alert("请设置日报每天提交时间！");
        return false;
    }

    if(day_detail_summary_time){
        
    }else{
        alert("请设置日报每天汇总时间！");
        return false;
    }

    if(week_detail_create_time){
        
    }else{
        alert("请设置周报每天提交时间！");
        return false;
    }

    if(week_detail_summary_time){
        
    }else{
        alert("请设置周报每天汇总时间！");
        return false;
    }

    if(day_detail_remind_interval){
        
    }else{
        alert("请设置日报提醒周期！");
        return false;
    }

    if(week_detail_remind_interval){
        
    }else{
        alert("请设置周报提醒周期！");
        return false;
    }
    if(day_detail_create_time >= day_detail_summary_time){
        alert("日报创建时间必须在汇总时间之前！");
        return false;
    }

    if(week_detail_create_time >= week_detail_summary_time){
        alert("周报创建时间必须在汇总时间之前！");
        return false;
    }
    return true;

}

function check_name(name)
{
    if(name){
            
    }else{
        alert("请填写项目组名称.");
        return false;
    }
    return true;
}

function check_task(member_task_summary_time, team_task_summary_time)
{
    if(member_task_summary_time){
            
    }else{
        alert("请设置个人任务汇总发布时间.");
        return false;
    }

    if(team_task_summary_time){
        
    }else{
        alert("请设置团队任务汇总发布时间.");
        return false;
    }
    return true;
}

function check_member(members)
{
    var l = members.length;
    if(l == 0){
        alert("请添加成员");
        return false;
    }
    var emailList = [];
    var nameList = [];
    for(var i=0; i<l;i++){
        var m = members[i];
        if(m["email"].length == 0){
            alert("成员邮件不能为空.");
            return 0;
        }
        if(m["name"].length == 0){
            alert("成员名字不能为空.");
            return 0;
        }
        var _f = isEmail(m["email"]);
        if(!_f){
            alert("成员邮件格式错误.");
            return false;
        }
        if($.inArray(m["email"], emailList) != -1){
            alert("User email repeat.");
            return false;
        }
        if($.inArray(m["name"], nameList) != -1){
            alert("User name repeat.");
            return false;
        }
        emailList.push(m["email"]);
        nameList.push(m["name"]);
    }
    return true;
}


function postNewTeam(){

    var day_or_week_str = $("#new_day_or_week_ul").find('li.cur').html();
    var day_or_week = 0;
    if (day_or_week_str == "周报"){
        day_or_week = 1;
    }

    var _week_detail_create_time = $("#datetimepicker4").val();
    var _week_detail_summary_time = $("#datetimepicker5").val();
    var _new_team_week_week_create_time = get_r_week($("#new_team_week_week_create_time").html());
    var _new_team_week_week_summary_time = get_r_week($("#new_team_week_week_summary_time").html());

    var name = $.trim($("#new_teamname").val());

    var day_detail_create_time = $("#datetimepicker1").val();
    var day_detail_summary_time = $("#datetimepicker3").val();

    var member_task_summary_time = $("#datetimepicker6").val();
    var team_task_summary_time = $("#datetimepicker7").val();

    var week_detail_create_time = _new_team_week_week_create_time + "-" + _week_detail_create_time;
    var week_detail_summary_time = _new_team_week_week_summary_time + "-" + _week_detail_summary_time;


    var day_detail_remind_interval = parseInt($("#new_team_day_remind_interval").find('li.cur').html());
    if (day_detail_remind_interval == 1){
        day_detail_remind_interval = 60;
    }

    var week_detail_remind_interval = parseInt($("#new_team_week_remind_interval").find('li.cur').html());
    if (week_detail_remind_interval == 1){
        week_detail_remind_interval = 60;
    }
    var members = [];
    var i = 0;
    var $members_dds = $("#members").find('dd').each(function(a){
        var member = {};
        var email = $(this).find('input.addsub_email').val();
        var username = $(this).find('input.addsub_username').val();
        var role = $(this).find('p.add_role').html();
        if(role == "组员"){
            role = "0";
        }else{
            role = "1";
        }
        member["email"] = $.trim(email);
        member["name"] = $.trim(username);
        member["role"] = role;
        members[i] = member;
        i++;
    })
    var flag1 = check_name(name);
    var flag2 = check_member(members);
    var flag3 = check_task(member_task_summary_time, team_task_summary_time);
    var flag4 = check_day_week(day_detail_create_time, day_detail_summary_time, week_detail_create_time, week_detail_summary_time, day_detail_remind_interval, week_detail_remind_interval);
    var flag = flag1 && flag2 && flag3 && flag4;
    if(!flag) return;

    var data = {
            "name": name,
            "day_detail_create_time": day_detail_create_time,
            "day_detail_summary_time": day_detail_summary_time,

            "member_task_summary_time": member_task_summary_time,
            "team_task_summary_time": team_task_summary_time,

            "week_detail_create_time": week_detail_create_time,
            "week_detail_summary_time": week_detail_summary_time,

            "day_detail_remind_interval": day_detail_remind_interval,
            "week_detail_remind_interval": week_detail_remind_interval,

            "day_or_week":day_or_week,

            "members": dump_json(members)
        }

    console.log(data);

    $.ajax({
        type: 'POST',
        url: "/createteam",
        data: data,
        dataType: 'text',
        success: function(res) {
            console.log(res);
            if (res == "Success"){
                location.href ="/";
            }else{
                alert(res);
            }
        },
        error: function(res) {
            console.log("Error");
        },
        complete: function() {
            console.log("Complete");
        }
    });
}

function click_del(username, useremail, teamname, role, options){
    // if(role > 1){
    //     alert("不能删除小组所有者!");
    //     return false;
    // }
    var defaults={
        oMembers:".members",
        oLi:"li",
        giveup:{div:"giveup",txt:"确定将"+username+"由"+teamname+"中移除？"},
    }
    var options= $.extend(defaults,options);
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
            var _This=$(this);
            _this.oLi.find("b").removeClass("cur");
            _This.addClass("cur");
            $(".popbg").css({"z-index":"100","display":"block"});
            _this.creatGiveup().appendTo($(document.body));
            $("#"+_this.oGiveup.div).css({top:$(window).height()/2-$(".giveup").outerHeight()/2+$(window).scrollTop(),left:$(window).width()/2-$(".giveup").outerWidth()/2+$(window).scrollLeft()});
            
            $("#"+_this.oGiveup.div).find(".btn").find("a").eq(0).click(function(){
                del_user_action(useremail);
                $("#"+_this.oGiveup.div).remove();
                _This.parent("li").remove();
                $(".popbg").css({"z-index":"98","display":"none"});
            })
            $("#"+_this.oGiveup.div).find(".btn").find("a").eq(1).click(function(){
                $("#"+_this.oGiveup.div).remove();
                $(".popbg").css({"z-index":"98","display":"none"});
                _this.oLi.find("b").removeClass("cur");
            })
        },
        Position:function(){
            $("#"+this.oGiveup.div).css({top:$(window).height()/2-$(".giveup").outerHeight()/2+$(window).scrollTop(),left:$(window).width()/2-$(".giveup").outerWidth()/2+$(window).scrollLeft()});
        }        
    }    
    Mantle.init();
    $(window).bind("resize",function(){
        Mantle.Position();
    }) 
}

function del_user_action(useremail)
{
    $.ajax({
        type: 'DELETE',
        data: {
            "useremail": useremail
        },
        dataType: 'text',
        success: function(res) {
            console.log(res);
            if (res == "Success"){
                location.reload();
            }else{
                alert(res);
            }
        },
        error: function(res) {
            console.log("Error");
        },
        complete: function() {
            console.log("Complete");
        }
    });
}

function add_user_action()
{
    var members = [];
    var i = 0;
    var $members_dds = $("#add_members").find('dd').each(function(a){
        var member = {};
        var email = $(this).find('input.addsub_email').val();
        var username = $(this).find('input.addsub_username').val();
        var role = $(this).find('p.add_role').html();
        if(role == "组员"){
            role = "0";
        }else{
            role = "1";
        }
        member["email"] = $.trim(email);
        member["name"] = $.trim(username);
        member["role"] = role;
        members[i] = member;
        i++;
    })

    var flag = check_member(members);
    if(!flag){
        return false;
    }
    
    $.ajax({
        type: 'PUT',
        data: {
            "members": dump_json(members)
        },
        dataType: 'text',
        success: function(res) {
            console.log(res);
            if (res == "Success"){
                location.reload();
            }else{
                alert(res);
            }
        },
        error: function(res) {
            console.log("Error");
        },
        complete: function() {
            console.log("Complete");
        }
    });
}

function set_detail_status_day(ts, detailID){
    var status_str = ($(ts).find('#detailStatus').html());
    var status = 0;
    if (status_str == "已请假"){
        status = 3;
    }
    else if(status_str == "已提醒"){
        status = 1;
    }
    else if (status_str == "已提交")
    {
        status = 2;
    }
    else{
        status = 0;
    }

    $.ajax({
        type: 'POST',
        url: '/detail/day/',
        data: {
            "detailID": detailID,
            "status": status
        },
        dataType: 'text',
        success: function(res) {
            console.log(res);
            if (res == "Success"){
                console.log("Success");
            }else{
                alert(res);
            }
        },
        error: function(res) {
            alert("Error");
        },
        complete: function() {
            console.log("Complete");
        }
    });
}

function set_detail_status_week(ts, detailID){
    var status_str = ($(ts).find('#detailStatus').html());
    var status = 0;
    if (status_str == "已请假"){
        status = 3;
    }
    else if(status_str == "已提醒"){
        status = 1;
    }
    else if (status_str == "已提交")
    {
        status = 2;
    }
    else{
        status = 0;
    }

    $.ajax({
        type: 'POST',
        url: '/detail/week/',
        data: {
            "detailID": detailID,
            "status": status
        },
        dataType: 'text',
        success: function(res) {
            console.log(res);
            if (res == "Success"){
                console.log("Success");
            }else{
                alert(res);
            }
        },
        error: function(res) {
            alert("Error");
        },
        complete: function() {
            console.log("Complete");
        }
    });
}


function updateTeam()
{
    var _week_detail_create_time = $("#datetimepicker10").val();
    var _week_detail_summary_time = $("#datetimepicker12").val();
    var _update_team_week_week_create_time = get_r_week($("#update_team_week_week_create_time").html());
    var _update_team_week_week_summary_time = get_r_week($("#update_team_week_week_summary_time").html());

    var day_detail_create_time = $("#datetimepicker8").val();
    var day_detail_summary_time = $("#datetimepicker99").val();

    var week_detail_create_time = _update_team_week_week_create_time + "-" + _week_detail_create_time;
    var week_detail_summary_time = _update_team_week_week_summary_time + "-" + _week_detail_summary_time;

    var day_detail_remind_interval = parseInt($("#update_team_day_remind_interval").find('li.cur').html());
    if (day_detail_remind_interval == 1){
        day_detail_remind_interval = 60;
    }

    var week_detail_remind_interval = parseInt($("#update_team_week_remind_interval").find('li.cur').html());
    if (week_detail_remind_interval == 1){
        week_detail_remind_interval = 60;
    }

    var day_or_week_str = $("#update_day_or_week_ul").find('li.cur').html();
    var day_or_week = 0;
    if (day_or_week_str == "周报"){
        day_or_week = 1;
    }

    var flag = check_day_week(day_detail_create_time, day_detail_summary_time, week_detail_create_time, week_detail_summary_time, day_detail_remind_interval, week_detail_remind_interval);
    if(!flag) return;

    url = "/teamaction/" + $("#thisteamid").html();

    $.ajax({
        type: 'PUT',
        url: url,
        data: {
            "day_detail_create_time": day_detail_create_time,
            "day_detail_summary_time": day_detail_summary_time,

            "week_detail_create_time": week_detail_create_time,
            "week_detail_summary_time": week_detail_summary_time,

            "day_detail_remind_interval": day_detail_remind_interval,
            "week_detail_remind_interval": week_detail_remind_interval,

            "day_or_week": day_or_week
        },
        dataType: 'text',
        success: function(res) {
            console.log(res);
            if (res == "Success"){
                location.reload();
            }else{
                alert(res);
            }
        },
        error: function(res) {
            console.log("Error");
        },
        complete: function() {
            console.log("Complete");
        }
    });
}