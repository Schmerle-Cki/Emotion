export function getImageList(){
	const path = require('path');
	//let count = 0;
	let imgs = [];
	const files1 = require.context('../img/practiceCartoon',true,/.jpg$/);
	files1.keys().forEach(item=>{			
		imgs.push(path.basename(item,'.jpg'));				
	});
	// RealMan Practice
	const files2 = require.context('../img/practiceReal',true,/.jpg$/);
	files2.keys().forEach(item=>{			
		imgs.push(path.basename(item,'.jpg'));				
	});
	const files = require.context('../img/formal',true,/.jpg$/);
	files.keys().forEach(item=>{
		imgs.push(path.basename(item,'.jpg'));		
	});	
		
	/*for (let img of imgs) {
		let image = new Image();
		image.src = img;
		image.onload = () => {
			count++;
		};
	}*/	
	return imgs;
}