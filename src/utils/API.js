const API={
    GET_MESSAGE_LIST:{
        path:process.env.VUE_APP_URL + "/api/message",
        method:"get"
    },
    POST_NEW_MESSAGE:{
        path:process.env.VUE_APP_URL + "/api/message",
        method:"post"
    },
}

export default API