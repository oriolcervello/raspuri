var origwidth=600
var origheight=800
var Sorigwidth=600
var Sorigheight=800
var origtime = 11
var minh=9
var maxh=16
function IMG(prefix, region, date, param, time, png,ht,wid)
{
//rasp - replace model with date
  this._date = date;
//blip  this._model = model;
  this._region = region;
  this._prefix = prefix;
  this._param = param;
//rasp - add day field, force day to curr
  this._day = "curr";
  this._time = time;
  this._showwn = false;
  this._png = png;
  this._ht = ht;
  this._wid = wid;
}
IMG.prototype.getUrl = function ()
{
  with (this) {
    var imgUrl = "";
    timestr=("0" + _time).slice(-2)
    imgUrl = _prefix+_region+"/"+_date+"/"+_param+timestr+_png 
    }
    return imgUrl;
}
IMG.prototype.show = function ()
{
//document.write("<p>"+this._ht+" width="+this._wid+" "+this.getUrl()+"</p>");
timestr=("0" + this._time).slice(-2)
name=this._param+timestr+this._png;
document.write("<IMG src=\""+this.getUrl()+"\" alt=\""+name+"\" class=\"w3-image\" height=\""+this._ht+"\" width=\""+this._wid+"\" id=\"RASPimage\">");

}

var IMG = new IMG("OUT/plot/", "dom01", "20200118", "Ager Desp._", origtime, ".png",origheight,origwidth)

function currentIMG()
{
  return IMG;
}
function showRegion(region)
{  
  document.getElementById(IMG._region).className ="w3-xlarge w3-text-grey w3-hover-black";
  IMG._region = region;
  document.getElementById(region).className ="w3-xlarge w3-black w3-hover-black";
  load_js();
}
function showPrefix(prefix)
{
  IMG._prefix = prefix;
  load_js();
}
function showTime(time)
{  
  bstr= "b"+IMG._time;
  document.getElementById(bstr).className ='w3-black';
  bstr= "b"+time;
  document.getElementById(bstr).className ='w3-light-grey'  ;
  IMG._time = time;
  load_js();
}
function showParam(param)
{ 
  IMG._ht = origheight;
  IMG._wid = origwidth;
  IMG._param = param;
  load_js();
}
function advancetime(hours)
{
  bstr= "b"+IMG._time;
  document.getElementById(bstr).className ='w3-black';
  var time=IMG._time+hours;
  if (time < minh) {
    time=minh;
  }
  if (time > maxh) {
    time=maxh;
  } 
  IMG._time=time;
  bstr= "b"+IMG._time;
  document.getElementById(bstr).className ='w3-light-grey';
  load_js();
}
function showSkew(param)
{ 
  IMG._ht = Sorigheight;
  IMG._wid = Sorigwidth;
  IMG._param = param;
  load_js();
  //adjustImgSz(0.85);
}
function showdate(date)
{ 

  document.getElementById((IMG._date).slice(-2)).className ='w3-black w3-large';
  var n =  new Date();
  var mili = n.getTime();
  n =  new Date(mili+date*(24*3600*1000)); 
  var y = n.getUTCFullYear();
  var m = n.getUTCMonth() + 1;
  m = ("0" + m).slice(-2);
  var d = n.getUTCDate();
  d = ("0" + d).slice(-2);

  IMG._date = y+m+d;
  document.getElementById(d).className ='w3-light-grey w3-large';
  load_js();
}

function adjustImgSz(fctr)
{
  
  IMG._ht *= fctr;
  IMG._wid *= fctr;
  load_js();
}
function origImgSz()
{
  
  IMG._ht = origheight;
  IMG._wid = origwidth;
  load_js();
}

function initshow()
{  
  
  //window.IMG = new IMG("OUT/plot/", "dom01", "20200118", "cloudlow", "09", ".png",700,400)

  bstr= "b"+origtime;
  var n =  new Date();
  var y = n.getUTCFullYear();
  var m = n.getUTCMonth() + 1;
  m = ("0" + m).slice(-2);
  var d = n.getUTCDate();
  d = ("0" + d).slice(-2);
  IMG._date = y+m+d;
  IMG.show();

  window.addEventListener('load', function () { 
      document.getElementById(bstr).className ='w3-light-grey';
      document.getElementById(d).className ='w3-light-grey w3-large';
      document.getElementById(IMG._region).className ="w3-xlarge w3-black w3-hover-black";
  })
}



function load_js() {
 
 document.getElementById('RASPimage').src=IMG.getUrl();
 document.getElementById('RASPimage').width =IMG._wid;
 document.getElementById('RASPimage').height =IMG._ht;
 timestr=("0" + IMG._time).slice(-2);
 document.getElementById('RASPimage').alt =IMG._param+timestr+IMG._png;
 
}
       
function download() {
  var element = document.createElement('a');
  element.setAttribute('href', IMG.getUrl());
  timestr=("0" + this._time).slice(-2)
  name=this._param+timestr+this._png;
  element.setAttribute('download', name);
  element.setAttribute('target', "_blank");
  
  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}
