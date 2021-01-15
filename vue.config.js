module.exports = {
  devServer: {
	// Path
	//baseUrl: './',	
	host:'www.cartoonEmotion.com',
	disableHostCheck: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000', // 修改为你的Django服务器地址
        changOrigin: true,
      }
    }	
  }  
}
