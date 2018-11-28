package 
{
	import flash.display.MovieClip;
	import fl.controls.Button;
	import fl.controls.Label;
	import fl.events.ComponentEvent;
	import flash.display.*;
	import flash.events.*;
	import flash.geom.*;
	import flash.text.*;
	import flash.events.MouseEvent;
	import fl.controls.Button;//MovieClip
	import flash.net.FileReference;
	import flash.net.FileReference.*;
	import flash.display.Bitmap;
	import flash.display.BitmapData;
	import flash.net.FileFilter;
	import flash.display.Loader;
	import flash.net.URLRequest;
	import flash.net.*;
	import 	fl.video.*;
	import flash.geom.Matrix;
	import flash.display.Sprite; 
	 import flash.text.TextField; 
	 import flash.text.TextFieldAutoSize; 
	 import flash.text.TextFormat; 
	public class demoScript extends flash.display.Sprite
	{
		private var bt1:Button;
		private var file:FileReference=new FileReference();
		private var fileRef:FileReference= new FileReference();
		private var loader:Loader = new Loader();
		private var buttonShape:Shape = new Shape();
		var recMatrix= new Matrix();
		var myText0:TextField = new TextField  ;
		var myText1:TextField = new TextField  ;	
		var myText_b:TextField = new TextField  ;
		var myText_as:TextField = new TextField  ;
		var myText_bs:TextField = new TextField  ;
		//var loader.loader=new Loader();
		public function demoScript()
		{	
			myText_as.border = true;
			myText_as.type = TextFieldType.INPUT;
			myText_as.restrict = "0-5";
			myText_as.maxChars = 3;
			addChild(myText_as);
			myText_as.width = 40;
			myText_as.height = 20;
			myText_as.x=300;
			myText_as.y=50;
			myText_as.addEventListener(Event.CHANGE,ab);
		
			myText_bs.border = true;
			myText_bs.type = TextFieldType.INPUT;
			myText_bs.restrict = "0-5";
			myText_bs.maxChars = 3;
			addChild(myText_bs);
			myText_bs.width = 40;
			myText_bs.height = 20;
			myText_bs.x=340;
			myText_bs.y=50;
			myText_bs.addEventListener(Event.CHANGE,ab);
		
		
		
		
			myText_b.border = true;
			myText_b.type = TextFieldType.INPUT;
			myText_b.restrict = "0-9";
			myText_b.maxChars = 3;
			addChild(myText_b);
			myText_b.width = 40;
			myText_b.height = 20;
			myText_b.x=100;
			myText_b.y=500;
			myText_b.addEventListener(Event.CHANGE,degree);
		
		
			//0:Y 1:X
			myText0.border = true;
			myText0.type = TextFieldType.INPUT;
			myText0.restrict = "0-9";
			myText0.maxChars = 4;
			addChild(myText0);
			myText0.width = 60;
			myText0.height = 20;
			myText0.x=100;
			myText0.y=600;
			myText1.border = true;
			myText1.type = TextFieldType.INPUT;
			myText1.restrict = "0-9";
			myText1.maxChars = 4;
			addChild(myText1);
			myText1.width = 60;
			myText1.height = 20;
			myText1.x=100;
			myText1.y=550;
			myText1.addEventListener(Event.CHANGE,pd);
			myText0.addEventListener(Event.CHANGE,pd);
			var loc1:* = null;
			var loc2:* = null;
			var loc3:* = null;
			var loc4:* = null;
			//BGraund = new flash.display.Sprite();
			todSprite = new flash.display.Sprite();
			smoke = new smokeScript(350,200,16711935,100,0.0041);
			plz0 = new toddlerScript(80,40);
			plz1 = new toddlerScript(100,50);
			plz2 = new toddlerScript(255,0);//烟雾数值
			plz3 = new toddlerScript(255,0);
			plz4 = new toddlerScript(255,0);
			PachNFi = new flash.text.TextField();
			PachNFo = new flash.text.TextFormat();
			AlphaVFi = new flash.text.TextField();
			AlphaVFo = new flash.text.TextFormat();
			ColorPcRFi = new flash.text.TextField();
			ColorPcRFo = new flash.text.TextFormat();
			ColorPcGFi = new flash.text.TextField();
			ColorPcGFo = new flash.text.TextFormat();
			ColorPcBFi = new flash.text.TextField();
			ColorPcBFo = new flash.text.TextFormat();
			ColorPcFi = new flash.text.TextField();
			ColorPcFo = new flash.text.TextFormat();
			super();
			stage.frameRate = 40;
			//loc1 = new flash.geom.Matrix();
			//loc1.createGradientBox(590, 300, 0, 0, 0);
			//loc2 = [21504,602906];
			//loc3 = [1,1];
			//loc4 = [0,255];
			///BGraund.graphics.lineStyle(0.25, 0, 1);
			//BGraund.graphics.beginGradientFill(flash.display.GradientType.LINEAR, loc2, loc3, loc4, loc1);
			//BGraund.graphics.drawRect(0, 0, 590, 300);
			//BGraund.graphics.endFill();
			//addChild(BGraund);
			addChild(menu1);
			todSprite.addChild(plz0.toddlerShow(20, 235));
			PachNFo.bold = true;
			PachNFo.size = 16;
			PachNFo.color = 5592439;
			PachNFi.autoSize = flash.text.TextFieldAutoSize.LEFT;
			addChild(PachNFi);
			PachNFi.x = 20;
			PachNFi.y = 210;
			PachNFi.setTextFormat(PachNFo);
			todSprite.addChild(plz1.toddlerShow(20, 270));
			AlphaVFo.bold = true;
			AlphaVFo.size = 16;
			AlphaVFo.color = 5592439;
			AlphaVFi.autoSize = flash.text.TextFieldAutoSize.LEFT;
			addChild(AlphaVFi);
			AlphaVFi.x = 20;
			AlphaVFi.y = 245;
			AlphaVFi.setTextFormat(AlphaVFo);
			ColorPcFo.bold = true;
			ColorPcFo.size = 14;
			ColorPcFo.color = 5592439;
			ColorPcFi.autoSize = flash.text.TextFieldAutoSize.LEFT;
			addChild(ColorPcFi);
			ColorPcFi.x = 15;
			ColorPcFi.y = 60;
			ColorPcFi.setTextFormat(ColorPcFo);
			todSprite.addChild(plz2.toddlerShow(20, 100));	
			ColorPcRFo.bold = true;
			ColorPcRFo.size = 14;
			ColorPcRFo.color = 5592439;
			ColorPcRFi.autoSize = flash.text.TextFieldAutoSize.LEFT;
			addChild(ColorPcRFi);
			ColorPcRFi.x = 20;
			ColorPcRFi.y = 80;
			ColorPcRFi.setTextFormat(ColorPcRFo);
			todSprite.addChild(plz3.toddlerShow(20, 140));
			ColorPcGFo.bold = true;
			ColorPcGFo.size = 14;
			ColorPcGFo.color = 5592439;
			ColorPcGFi.autoSize = flash.text.TextFieldAutoSize.LEFT;
			addChild(ColorPcGFi);
			ColorPcGFi.x = 20;
			ColorPcGFi.y = 120;
			ColorPcGFi.setTextFormat(ColorPcGFo);
			todSprite.addChild(plz4.toddlerShow(20, 180));
			ColorPcBFo.bold = true;
			ColorPcBFo.size = 	14;
			ColorPcBFo.color = 5592439;
			ColorPcBFi.autoSize = flash.text.TextFieldAutoSize.LEFT;
			addChild(ColorPcBFi);
			ColorPcBFi.x = 20;
			ColorPcBFi.y = 160;
			ColorPcBFi.setTextFormat(ColorPcBFo);
			fon.graphics.lineStyle(1, 0, 1);
			fon.graphics.beginFill(3355443, 0);
			// fon.graphics.drawRect(0, 0, 800, 600);
			fon.graphics.endFill();
			addChild(fon);
			addChild(todSprite);
			addChild(smoke.FnSmoke());
			addEventListener(flash.events.Event.ENTER_FRAME, FnGoPl);
			recMatrix =smoke.smokeSprite.transform.matrix;	
			//bt1.addEventListener(MouseEvent.CLICK, Kn);
			//addChild(bt1);
			Kn();
			//bt1.onButtonClick();
			return;
		}

		public function pd(e:Event):void{
		//trace(myText0.text.length,myText1.text.length);
			if (myText0.text.length!=0 && myText1.text.length!=0)
			{
				//trace("已单击鼠标");
				smoke.smokeSprite.x =myText1.text;
				smoke.smokeSprite.y = myText0.text;
				//smoke.tra
			}

			return;
		}
		public function ab(e:Event):void{
		if (myText_as.text.length!=0 )
			{
				recMatrix.a =myText_as.text;
			}
		else{recMatrix.b =1;}
		
		if (myText_bs.text.length!=0 )
			{
				recMatrix.b =myText_bs.text;
			}
		else{recMatrix.b =1;}
		smoke.smokeSprite.transform.matrix = recMatrix;
		return;
		}
		
		public function pds():void{
		//trace(myText0.text.length,myText1.text.length);
			if (myText0.text.length!=0 && myText1.text.length!=0)
			{
				//trace("已单击鼠标");
				smoke.smokeSprite.x =myText1.text;
				smoke.smokeSprite.y = myText0.text;

			}

			return;
			
		
		}
		
		var te:int=0;
		public function degree(e:Event):void
		{
			trace(Math.tan(Math.PI/180*45))
			trace(myText_b.text);
			if (myText_b.text.length!=0){
			
				// if (myText_b.text)
				// trace('OK');
				// //smoke.v_YS = 2 * Math.random();
				// smoke.v_XS = 2;
				// trace("Y:",smoke.v_YS);
				// //smoke.arrayPach[0].vy =smoke.v_YS;
				// var z =(Math.tan(Math.PI/180*(myText_b.text)));
				// trace("z:",z)
				// //smoke.v_XS = (0.5+0.5*smoke.v_YS)/(z*0.05)/10.0;
				// smoke.v_YS =smoke.v_XS*z;
				// //smoke.arrayPach[0].vx = smoke.v_XS ;
				// trace(z,smoke.v_YS,smoke.v_XS);
			recMatrix.rotate(Math.PI/180*Math.abs(360-te));
			smoke.smokeSprite.transform.matrix = recMatrix;
			//var tt:Matrix = new Matrix();
			//tt = recMatrix;
			te = myText_b.text 
			
			//recMatrix.a =1;
			//recMatrix.b =2;
			//recMatrix.translate(200,200);
			recMatrix.rotate(Math.PI/180*myText_b.text);
			// recMatrix.translate(200,200)
			smoke.smokeSprite.transform.matrix = recMatrix;
			pds();
			}
			else
			{
				
			}
			// if (myText_b >90&&myText_b<=180)
			// {	smoke.XS = -1
				// smoke.YS = -1
				// smoke.v_YS = Math.floor(2 * Math.random());
				// smoke.arrayPach[0].vx = (0.5+0.5*smoke.v_YS)/(Math.tan(myText_b)*0.05);
				// smoke.
			// }
			
			return;
		}

		//切换背景
		internal function Kn():void
		{
			// 开始您的自定义代码
			// 此示例代码在"输出"面板中显示"已单击鼠标"。
			//var file:FileReference=new FileReference();
			//设置文字
		   var textBox:TextField = new TextField(); 
			textBox.background=true;
		   textBox.text = "切换背景"; 
		   textBox.autoSize = TextFieldAutoSize.CENTER; 
		   textBox.embedFonts=true; 
		   //textBox.backgroundColor=0xff0000;
		   //addChild(textBox); 
		   var formatter:TextFormat = new TextFormat(); 
		      //formatter.font = "xjl"; 
			formatter.size = 30; 
		   
			 textBox.setTextFormat(formatter); 
		   
			buttonShape.graphics.beginFill(0x336699);
			//buttonShape.graphics.drawCircle(30, 25, 25);
			buttonShape.graphics.drawRect(100,50,30,25);
			
			var button = new SimpleButton(buttonShape,buttonShape,buttonShape,buttonShape);
			button.alpha = 0.5;
			addChild(button);
			button.addEventListener(MouseEvent.CLICK, onButtonClick);

			function onButtonClick(e:MouseEvent):void
			{
				fileRef.browse([new FileFilter("Images", "*.jpg;*.gif;*.png")]);
				fileRef.addEventListener(Event.SELECT, onFileSelected);
				//smoke.smokeSprite.x =100;
				//smoke.smokeSprite.y =0

			}

			function onFileSelected(e:Event):void
			{
				//var loader:Loader = new Loader();
				// // loader.loadBytes(e.target.data);
									// // var bitmapData:BitmapData = _evt.target.content.bitmapData;
					
				
				
				//trace(loader.data);
				// var tempData:BitmapData=new BitmapData(loader.width,loader.height,
				                                                     // false,null);
				// tempData.draw(loader);
				// var bitmap:Bitmap = new Bitmap(tempData);
				
				// graphics.beginBitmapFill(Bitmap, new Matrix(), true, true);
					// graphics.drawRect(0, 0, stage.stageWidth, stage.stageHeight );

					// loader.contentLoaderInfo.removeEventListener(Event.COMPLETE , imageComplete);
					// loader = null;
				// addChild(bitmap);

				//
				fileRef.addEventListener(Event.COMPLETE, onFileLoaded);
				//fileRef.load();
				fileRef.load();
			}
			function test(e:Event):void
			{
				import flash.display.*;
				imgLoader("bg.jpg");
				var loader:Loader;
				function imgLoader(_path:String ):void
				{
					loader = new Loader  ;
					loader.contentLoaderInfo.addEventListener(Event.COMPLETE , imageComplete);
					loader.load(new URLRequest (_path));
					trace(loder);
				}
				function imageComplete(_evt:Event):void
				{
					var bitmapData:BitmapData = _evt.target.content.bitmapData;
					graphics.beginBitmapFill(bitmapData, new Matrix(), true, true);
					graphics.drawRect(0, 0, stage.stageWidth, stage.stageHeight );

					loader.contentLoaderInfo.removeEventListener(Event.COMPLETE , imageComplete);
					loader = null;
				}
			}

			function onFileLoaded(e:Event):void
			{
					
				//
				fileRef.removeEventListener(Event.COMPLETE,onFileLoaded);
				loader.contentLoaderInfo.addEventListener(Event.COMPLETE,onLoadComplete);
				loader.loadBytes(fileRef.data);
				//trace(loader.data);
				// var tempData:BitmapData=new BitmapData(loader.width,loader.height,
				                                                     // false,null);
				// tempData.draw(loader);
				// var bitmap:Bitmap = new Bitmap(tempData);
				// addChild(bitmap);

				//addChild(loader);
			}
		function onLoadComplete(e:Event):void
		{
			trace(stage.width,stage.height,loader.width,loader.height);
			var tempData:BitmapData=new BitmapData(1808,864,  //loder.
										false,null);
			//loader.scaleMode=StageScaEXACT_FIT;
			loader.content.width=1638;
			loader.content.height=864;
			tempData.draw(loader); //绘画
			//var bitmap:Bitmap = new Bitmap(tempData); //转换类型
			// addChild(bitmap);
			// loader.contentLoaderInfo.removeEventListener(Event.COMPLETE,
			                                                     // onLoadComplete);
																 
				// var bitmapData:BitmapData = _evt.target.content.bitmapData;
				mtr = new Matrix();
				mtr.tx=170;
				//mtr.a = stage.width/loader.width;
				//mtr.d = stage.height/loader.height;
					 graphics.beginBitmapFill(tempData, mtr, true, true);
					 graphics.drawRect(170, 0, 1638, 864 );//stageHeight 舞台大小变化小 两height变化大
					 loader.contentLoaderInfo.removeEventListener(Event.COMPLETE , onLoadComplete);
					 // loader = null;
		}
			//*/
			//trace("已单击鼠标");
			//trace(fileRef);
			//var directory:File = new File ; 
			// 结束您的自定义代码
		}


		internal function FnGoPl(arg1:flash.events.Event):void
		{
			var loc1:* = undefined;
			var loc2:* = undefined;
			var loc3:* = undefined;
			var loc4:* = undefined;
			var loc5:* = undefined;
			var loc6:* = undefined;
			smoke.PachN = plz0.nmb + 20;
			PachNFi.text = "PachN" + ":  " + smoke.PachN;
			PachNFi.setTextFormat(PachNFo);
			smoke.AlphaV = plz1.nmb / 10000;
			AlphaVFi.text = "AlphaV" + ":  " + plz1.nmb / 10000;
			AlphaVFi.setTextFormat(AlphaVFo);
			smoke.ColorR = plz2.nmb;
			smoke.ColorG = plz3.nmb;
			smoke.ColorB = plz4.nmb;
			ColorPcRFi.text = "redOffset" + ":  " + plz2.nmb;
			ColorPcRFi.setTextFormat(ColorPcRFo);
			ColorPcGFi.text = "greenOffset" + ":  " + plz3.nmb;
			ColorPcGFi.setTextFormat(ColorPcGFo);
			ColorPcBFi.text = "blueOffset" + ":  " + plz4.nmb;
			ColorPcBFi.setTextFormat(ColorPcBFo);
			loc1 = Math.floor(plz2.nmb / 16);
			loc2 = plz2.nmb % 16;
			loc3 = Math.floor(plz3.nmb / 16);
			loc4 = plz3.nmb % 16;
			loc5 = Math.floor(plz4.nmb / 16);
			loc6 = plz4.nmb % 16;
			ColorPcFi.text = "ColorPc" + ":  " + "0x" + loc1.toString(16) + loc2.toString(16) + loc3.toString(16) + loc4.toString(16) + loc5.toString(16) + loc6.toString(16);
			ColorPcFi.setTextFormat(ColorPcFo);
			return;
		}


		{
			fon = new flash.display.Sprite();
		};

		internal var ColorPcFi:flash.text.TextField;

		internal var plz3:toddlerScript;

		internal var ColorPcGFo:flash.text.TextFormat;

		internal var ColorPcGFi:flash.text.TextField;

		internal var plz2:toddlerScript;

		internal var BGraund:flash.display.Sprite;

		internal var ColorPcRFi:flash.text.TextField;

		internal var ColorPcBFi:flash.text.TextField;

		internal var smoke:smokeScript;

		internal var ColorPcRFo:flash.text.TextFormat;

		internal var todSprite:flash.display.Sprite;

		internal var ColorPcBFo:flash.text.TextFormat;

		public var menu1:flash.display.MovieClip;

		internal var PachNFi:flash.text.TextField;

		internal var PachNFo:flash.text.TextFormat;

		internal var AlphaVFi:flash.text.TextField;

		internal var AlphaVFo:flash.text.TextFormat;

		//internal var bt1:Button;

		internal var plz0:toddlerScript;

		internal var plz1:toddlerScript;

		internal var plz4:toddlerScript;

		internal var ColorPcFo:flash.text.TextFormat;

		public static var fon:flash.display.Sprite;
	}
}