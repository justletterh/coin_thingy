const {inspect}=require("util");
const mats=require("./mats.json");

function ename(v:any,e: any,full: boolean=false){
    var l=[];
    for (var i in e){
        l.push(i);
    }
    var h=Math.ceil(l.length/2);
    v=l.splice(0,h)[v];
    var k=l.splice(-h)[v];
    if (full){
        return [k,v];
    }else{
        return k;
    }
}

function cap(s){
    return s.charAt(0).toUpperCase()+s.slice(1);
}

enum Type{
    wood,
    metal,
    other
}

class Mat {
    type: {
        value: Type,
        name: string
    };
    lb: number;
    name: string;
    mat: string;
    
    constructor(name: string,type: Type,lb: number){
        this.type={
            value: type,
            name: ename(type,Type)
        };
        this.lb=lb;
        this.mat=name;
        this.name=this.procname(name);
    }

    procname(name: string){
        name=cap(name);
        if (this.type.value===Type.wood){
            var t="Wood ";
        }else{
            var t="";
        }
        var o=`${name} ${t}Coin`;
        return o;
    }

    debug(){
        var l=["name","mat","type.name","type.value","lb"];
        var c=0;
        [this.name,this.mat,this.type.name,this.type.value,this.lb].forEach(function(i){
            console.log();
            console.log(l[c]);
            console.log(i);
            console.log(typeof(i));
            c++;
        });
        return null;
    }
}

const metal=mats.metal;
const wood=mats.wood;
const other=mats.other;
var all=[];

var c=0;

var tmp=["metal","wood","other"];
[metal,wood,other].forEach(function(i){
    var t=Type[tmp[c]];
    for (var k in i){
        var v=i[k];
        all.push(new Mat(k,t,v));
    }
    c++;
});

console.log(all);