var origtime = 12
var minh=9
var maxh=16
var Overlay
var bounds1 = [[ 40.489006, -2.4023743], [ 44.1811, 4.676361]];
var bounds2 = [[ 40.99739, -0.023239613], [ 42.98399, 3.2804303]];
function IMG(prefix, region, date, param, time, png,bounds)
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
  this._bounds = bounds;
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
IMG.prototype.curbounds = function ()
{
  return this._bounds;
}
IMG.prototype.legendUrl = function ()
{
  with (this) {
    var imgUrl = "";
    timestr=("0" + _time).slice(-2)
    imgUrl = _prefix+_region+"/"+_date+"/"+_param+timestr+'L'+_png 
    }
    return imgUrl;
}
IMG.prototype.show = function ()
{
//document.write("<p>"+this._ht+" width="+this._wid+" "+this.getUrl()+"</p>");
timestr=("0" + this._time).slice(-2)
name=this._param+timestr+this._png;
document.getElementById("showing").innerHTML = "Showing: "+name;
    
  var imageUrls = [
        this.getUrl()
    ];


    Overlay = L.imageOverlay( imageUrls, L.latLngBounds(this.curbounds()), {
        opacity: 1
    }).addTo(map);


    testLegend.addTo(map);

}
  
function currentIMG()
{
  return IMG;
}

function showRegion(region)
{  
  document.getElementById(IMG._region).className ="w3-xlarge w3-text-grey w3-hover-black";
  if (region == "dom01") {
    IMG._bounds=bounds1;
  } 
  if (region == "dom02") {
    IMG._bounds=bounds2;
  }
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
  IMG._param = param;
  load_js();
}
function showParamMob()
{ 
  
  var e = document.getElementById("selectparamlist");
  IMG._param =e.options[e.selectedIndex].value;
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
 
 if (map.hasLayer(Overlay)) {
        map.removeLayer(Overlay);
    }

timestr=("0" + IMG._time).slice(-2)
name=IMG._param+timestr+IMG._png;
document.getElementById("showing").innerHTML = "Showing: "+name;
    
var imageUrls = [
        IMG.getUrl()
    ];
 
 Overlay = L.imageOverlay( imageUrls, L.latLngBounds(IMG.curbounds()), {
        opacity: 0.7
    }).addTo(map);
    

 document.getElementById('RASPlegend').src=IMG.legendUrl();
 
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


var IMG = new IMG("OUT/plot/", "dom01", "20200428", "cloudlow_", origtime, ".png",bounds1)
console.log(IMG._bounds)
console.log(bounds1)
var map = L.map('map').setView([42, 1], 7);
  //L.esri.basemapLayer('Topographic').addTo(map);
var Esri_WorldTopoMap = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', {
	attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community'
}).addTo(map);;
var testLegend = L.control({
    position: 'topright'});
testLegend.onAdd = function(map) {
    var src = IMG.legendUrl();
    var div = L.DomUtil.create('div', 'info legend');
    div.innerHTML +=
        '<img src="' + src + '" alt="legend" height="400" id=\"RASPlegend\">';
    return div;
};
initshow();
       

