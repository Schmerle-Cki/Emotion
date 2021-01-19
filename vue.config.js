module.exports = {
  devServer: {	
	host:'www.cartoonEmotion.com',
	disableHostCheck: true,
    proxy: {
      '/api': {
        target: 'https://3639f20597.oicp.vip', // 修改为你的Django服务器地址
		//target:'',
        changOrigin: true,
		ws: true,
		pathRewrite:{
			'^/api': '/api'
		}
      }
    }	
  },
  publicPath:'./'
}
