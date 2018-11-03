package 
{
    import flash.display.*;
    import flash.events.*;
    import flash.geom.*;
    import flash.utils.*;
     import flash.geom.Matrix;
    public class smokeScript extends flash.display.Sprite
    {
        public function smokeScript(arg1:*, arg2:*, arg3:*, arg4:*, arg5:*)
        {
            var loc1:*=0;
            var loc2:*=null;
            smokeSprite = new flash.display.Sprite();
            PozX = 400;//原 400
            PozY = 300;
            point0 = new flash.geom.Point(0, 0);
            arrayPach = new Array();
            lengthArr = 160;
			// 烟雾初始显示比例 原0.1
            scaleMin = 0.3;
            Tm = 75;
            flagVector = 1;
            jug = new JUG();
            gene = new GENEL();
            TGn = 50;
            TTGn = 0;
            PachN = 50;
            AlphaV = 0.0007;
            ColorPc = 16777215;
            ColorR = 255;
            ColorG = 255;
            ColorB = 255;
            super();
            PozX = arg1;
            PozY = arg2;
            ColorPc = arg3;
            PachN = arg4;
            AlphaV = arg5;
            gene.alpha = 0;
           // addChild(smokeSprite);  //可注销
            lengthArr = PachN;
            loc1 = 0;
            while (loc1 < 500) 
            {
                loc2 = new PACH1();
                arrayPach[loc1] = loc2;
                arrayPach[loc1].scaleX = scaleMin;
                arrayPach[loc1].scaleY = scaleMin;
                arrayPach[loc1].x = point0.x;
                arrayPach[loc1].y = point0.y;
                arrayPach[loc1].rot = 0;
                arrayPach[loc1].vx = 0;
                arrayPach[loc1].vy = 0;
                arrayPach[loc1].alf = 0;
                arrayPach[loc1].visible = false;
                arrayPach[loc1].sc = 0;
                smokeSprite.addChild(arrayPach[loc1]);
                ++loc1;
            }
            addEventListener(flash.events.Event.ENTER_FRAME, FnSmokeUp1);
            FnSmokeTm();
            smokeSprite.addChild(gene);
            smokeSprite.addChild(jug);
            return;
        }
		
        internal function FnSmokeUp1(arg1:flash.events.Event):void
        {
            var loc1:*=0;
            loc1 = 0;
            while (loc1 < arrayPach.length) 
            {
                arrayPach[loc1].alpha = arrayPach[loc1].alpha - AlphaV;
                arrayPach[loc1].scaleX = arrayPach[loc1].scaleX + (0.005 + arrayPach[0].sc);//src =0.005//
                arrayPach[loc1].scaleY = arrayPach[loc1].scaleY + (0.005 + arrayPach[0].sc);//速度
                 arrayPach[loc1].y = arrayPach[loc1].y + (0.5 + 0.5 * arrayPach[loc1].vy);// +向下/0.5
                 arrayPach[loc1].x = arrayPach[loc1].x + 0.05 * arrayPach[loc1].vx;//0.05 //扩散
				 // // arrayPach[loc1].x = arrayPach[loc1].x + (0.5 + 0.1 * arrayPach[loc1].vy);//向右
                 // // arrayPach[loc1].y = arrayPach[loc1].y + 0.05 * arrayPach[loc1].vx;//向右
				 // arrayPach[loc1].x = -arrayPach[loc1].y + (0.5+0.1* arrayPach[loc1].vy);
				 // arrayPach[loc1].y = -arrayPach[loc1].x - (0.05* arrayPach[loc1].vx);//两个+ 右下    //++-- 右上//----左下
				
				//arrayPach[loc1].y = (arrayPach[loc1].y +YS* arrayPach[loc1].vy);
				//arrayPach[loc1].x = (arrayPach[loc1].x + XS* arrayPach[loc1].vx);
				 
				
                arrayPach[loc1].rotation = arrayPach[loc1].rotation + 0.7 * arrayPach[loc1].rot;//0.7//烟雾旋转
                ++loc1;
            }
            return;
        }

        public function FnSmoke():flash.display.Sprite
        {
            smokeSprite.x = PozX;
            smokeSprite.y = PozY;
            return smokeSprite;
        }

        internal function FnSmokeUp(arg1:flash.events.TimerEvent):void
        {
            var loc1:*=0;
            var loc2:*=null;
            var loc3:*=null;
            var loc4:*=null;
            var loc5:*=null;
            var loc6:*=null;
            if (TTGn < TGn) 
            {
                var loc7:*;
                TTGn++;
                gene.alpha = TTGn / TGn;
            }
            if (100 * Math.random() > 93) 
            {
                flagVector = -flagVector;
            }
            loc1 = Math.floor(4 * Math.random());
            if (loc1 == 0) 
            {
                loc2 = new PACH1();
                arrayPach.unshift(loc2); //将loc 添加到arrayPach 开头
            }
            if (loc1 == 1) 
            {
                loc3 = new PACH2();
                arrayPach.unshift(loc3);
            }
            if (loc1 == 2) 
            {
                loc4 = new PACH3();
                arrayPach.unshift(loc4);
            }
            if (loc1 == 3) 
            {
                loc5 = new PACH4();
                arrayPach.unshift(loc5);
            }
            colorPc = arrayPach[0].transform.colorTransform;
            colorPc.color = ColorPc;
            colorPc.redOffset = ColorR;
            colorPc.greenOffset = ColorG;
            colorPc.blueOffset = ColorB;
            arrayPach[0].transform.colorTransform = colorPc;
            arrayPach[0].rot = -3 + Math.floor(7 * Math.random());
			//arrayPach[0].rot = 10;
             arrayPach[0].vx = flagVector * Math.floor(5 * Math.random());
             arrayPach[0].vy = Math.floor(2 * Math.random());
			//trace(Math.random());
			//arrayPach[0].vx = v_XS;
            //arrayPach[0].vy = v_YS;
			
			//trace(v_XS,v_YS);
			
            //arrayPach[0].alf = 0.2 + 3 * Math.random();//0.2 + 0.3
			arrayPach[0].alf = 0.2 + 3 * Math.random();
            arrayPach[0].sc = 0.01 * Math.random();//0.001//绽放大小速度
            arrayPach[0].x = point0.x;
            arrayPach[0].y = point0.y;
			//arrayPach[0].x =0;
            //arrayPach[0].y = 0;
            arrayPach[0].scaleX = scaleMin;
            arrayPach[0].scaleY = scaleMin;
            smokeSprite.addChild(arrayPach[0]);
            smokeSprite.removeChild(arrayPach[(arrayPach.length - 1)]);
            arrayPach.pop();
            PachN = PachN;
            if (PachN > arrayPach.length) 
            {
                loc6 = new PACH1();
                arrayPach.unshift(loc6);
                arrayPach[0] = loc6;
                arrayPach[(length - 1)].scaleX = scaleMin;
                arrayPach[0].scaleY = scaleMin;
                arrayPach[0].x = point0.x;
                arrayPach[0].y = point0.y;
                arrayPach[0].rot = 0;
                arrayPach[0].vx = 0;
                arrayPach[0].vy = 0;
                arrayPach[0].alf = 0;
                arrayPach[0].visible = false;
                arrayPach[0].sc = 0;
                smokeSprite.addChild(arrayPach[0]);
            }
            if (PachN < (arrayPach.length - 1)) 
            {
                smokeSprite.removeChild(arrayPach[(arrayPach.length - 1)]);
                arrayPach.pop();
            }
            return;
        }

        internal function FnSmokeTm():void
        {
            SMT = new flash.utils.Timer(Tm);
            SMT.addEventListener(flash.events.TimerEvent.TIMER, FnSmokeUp);
            SMT.start();
            return;
        }
	
	
		public var XS:Number=1.0;
		public var YS:Number=-1.0;
		
		public var v_XS:Number= Math.floor(5 * Math.random());
		public var v_YS:Number=Math.floor(2 * Math.random());
        public var PachN:int=50;

        internal var smokeSprite:flash.display.Sprite;

        internal var gene:GENEL;

        internal var arrayPach:Array;

        public var AlphaV:Number=0.0007;

        internal var SMT:flash.utils.Timer;

        internal var TGn:int=50;

        public var ColorB:int=255;

        public var ColorG:int=255;

        public var ColorR:int=255;

        internal var jug:JUG;

        internal var PozX:int=400;

        internal var TTGn:int=0;

        internal var PozY:int=300;

        internal var Tm:int=175;

        public var ColorPc:int=16777215;

        internal var point0:flash.geom.Point;

        internal var scaleMin:Number=0.1;

        internal var lengthArr:int=60;

        internal var colorPc:flash.geom.ColorTransform;

        internal var flagVector:int=1;
    }
}
