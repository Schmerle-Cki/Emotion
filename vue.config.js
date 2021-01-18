module.exports = {
  devServer: {	
	host:'www.cartoonEmotion.com',
	disableHostCheck: true,
    proxy: {
      '/api': {
        target: 'http://36f9205z97.zicp.vip', // 修改为你的Django服务器地址
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
