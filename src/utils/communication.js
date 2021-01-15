/**
 * 如果需要修改为正常上线模式，请注释下面mock的import代码
 * **/
//import "@/mock/index"
import API from '@/utils/API.js'
import axios from 'axios'

 // 请在下方实现自己的后端通信函数
 
export function setCookie(name, expiredays){
    var exdate=new Date()
    exdate.setDate(exdate.getDate()+expiredays);
    document.cookie = "user="+name+((expiredays ==null)?"":";expires=" + exdate.toGMTString())
}

export function getCookie(){
    var arr, reg = new RegExp("(^| )" + "user" + "=([^;]*)(;|$)")
    arr = document.cookie.match(reg)
    if (arr)
        return (arr[2]);
    else
        return null;
}

export function GET_Message(){
    return new Promise((resolve,reject) =>{
        axios.get(API.GET_MESSAGE_LIST.path).then(response =>{
            resolve(response.data);
        }).catch(err =>{
            reject(err)
        })
    })
}

export function POST_Message(data){
    return new Promise((resolve,reject) =>{
        axios.post(API.POST_NEW_MESSAGE.path,data).then(response =>{
            resolve(response.data);
        },err => {
            reject(err)
        })
    })
}