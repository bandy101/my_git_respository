;The first program

(begin
    (display "Hello, World!")
    ;1.2
    (define x (+ (+ 5 4)
                 (- 2 
                    (- 3
                        (+  6 
                            (/ 4 5)))))
    )
    (define y (* (* 3 
                    (- 6 2))
                 (- 2
                    7))
    )
    (define result (/ x y))
    
    ;1.3
    (define (max_two_add x y z)
            (cond ((> (+ x y) (+ x z)) 
                        (cond((> (+ x y) (+ y z)) (+ x y))
                            (else (+ y z))))
                (else (cond((> (+ x z) (+ y z)) (+ x z))
                        (else (+ y z)))
                )
            ))
    ;max
    
    (define (max x_ y_ z_) 
        (cond ((> x_ y_)
                (cond ((> x_ z_) x_)
                     (else z_)))
             ((<= x_ y_)
                (cond ((> y_ z_) y_)
                      (else z_)
                      ))
            ;  (else x_)         
                    )
        )

        ; (define (<= x y)
        ; (or (< x y) (= x y)))
    (define (xxx a b c)
        (cond ((and (<= a b) (<= a c))   c)
                 ((and (<= b a) (<= b c))   (+ a c))
                 (else              
                                       (+ a b))))
    ;实例1.17 牛顿求根法
    (define (new-if p g x)
            (cond ((p) g)
             (else x)))

    (define (sqrt guess x)
            ; ( new-if (sqrt_cond guess (sqrt (/ (+ 
            ;                    (/ x guess)
            ;                     guess)
            ;                 2) 
            ;                     x))))
            (if (sqrt_cond guess x) 
                guess
                (sqrt (/ (+ 
                           (/ x guess)
                            guess)
                        2) 
                            x)))
    
    (define (sqrt_cond guess x)
            (< (abs(- (* guess guess) x)) 0.001))
    
    ;  (((y/g)+g)/2**2 -y)<value
    ;1.6 重新定义 正则序 (完全展开后归约) ：正则序的递归 会陷入死循环
    
    ;1.7
    (define (sqrt_cond_ie guess guess_)
            (< (/ (abs(- guess guess_)) guess) 0.001))
    (define (sqrt_ guess x)
            (define t (/ (+ 
                (/ x guess)
                 guess)
             2) )
            (if(sqrt_cond_ie guess t)
                guess
                (sqrt_ t  x))
    )
    ;1.8 (1.34 实现一般牛顿法)
    (define (cubic_cond_ie guess guess_)
            (< (/ (abs(- guess guess_)) guess) 0.001))
    (define (cubic y x)
                (define t (/ (+ (/ x (* y y))
                                (* y 2))
                                3))
                (if (cubic_cond_ie y t)   ;t 可替换成函数
                    y
                    (cubic t x))
    )   
    
    ;递归的执行：[执行器推迟执行（需要执行的）链条长度，对于阶乘，长度随n正比，这个过程：线性递归]
    ;对于阶乘，另外一种不会推迟执行的计算，而是将计算保存在一个轨迹中，这个过程：线性迭代

    ;1.9    
        ; (define (+ a b)
        ;         (if (= a 0)
        ;             b
        ;             (inc(+ (dec a) b))))  

        ;   (+ 4 5)
        ; -> inc (+ 3 5) ->
        ; |   inc(inc (+ 2 5))
        ; |   inc(inc(inc(+ 1 5)))
        ; |   inc(inc(inc(inc(+ 0 5))))
        ; |   inc(inc(inc(inc(5))))
        ; | 递归  推迟了轨迹的计算的执行
        ;   (define + a b)
                    ; (if (= a 0)
                    ;     b
                    ;     (+ dec(a) inc(b))))
        ; |   (+ 4 5) ->
        ; |   ( + 3 6) ->
        ; |   (+ 2 7) -> (+ 1 8) -> (+ 0 9) -> 9   
        ; |  迭代 轨迹保存于本身
        ; |
        ;practice 1.10

        (define (A x y)
                (cond ((= y 0) 0)
                      ((= x 0) (* 2 y))
                      ((= y 1) 2)
                      (else (A (- x 1)
                               (A x (- y 1))))))
        ;代换模式: (A 1 10)    2**N
        ;|         ->(A 0 (A 1 9))
        ;|            -> (A 0 (A 0 (A 1 8))) 
        ;|                -> (A 0 (A 0 (A 0 (A 1 7))) .......(A 0 (A 1 1)) =9[(A 0] (A 1 1))  ->2**9*2
        ;          (A 2 4):: (A 1 16)    ;(2**2)**(N-1)
        ;           ->(A 1 (A 2 3))         
        ;               -> (A 1 (A 1 (A 2 2)))
        ;                    ->(A 1 (A 1 (A 1 (A 2 1))))  -->(A 1 (A 1 (A 1 2)) -->(A 1 (A 1 4)) --> (A 1 2**4) ->(A 1 16) = 2**16
        ;          (A 3 3)
        ;           ->(A 2 (A 3 2))
        ;              ->(A 2 (A 2 (A 3 1)))
        ;                 ->(A 2 (A 2 2)) -> (A 2 4) ->(A 1 16) 2**16
        ;|  2**2**2**2      U = 2 **N

        ; practice 1.11
        ; 递归ways
        (define (f n)
                (if (< n 3)
                        n
                        (+ (f (- n 1))
                                (* (f (- n 2)) 2)
                           (* (f (- n 3))
                                3))))
        ;f(3)+2*f(2)+3*f(1)=7+f(3) =7+ f(2) +2*f(1)+3*f(0) =14 ok
        ;迭代ways
        (define (F n)
                (define k n)
                (f_iter 0 1 2 k n))
        (define (f_iter a b c k n)
                (define z (* a 3))
                (define x (* b 2))
                (define s (+ z x c))
                (if (< n 3)
                 k
                 (f_iter b c s s (- n 1))
                ))
                
        ;(F 4)->(f 0 1 2 4 4)->(f 1 2 2*1+2(4) s 3)->(f 2 4 2*2+3*1+4 s 2)
        
        ;practice 1.12   ;;求每个元素
        ; # row:
; # 0        1
; # 1       1 1
; # 2      1 2 1
; # 3     1 3 3 1
; # 4    1 4 6 4 1
; # 5   . . . . . .
; # col: 0 1 2 3 4
; (row col)=row!col!⋅(row−col)!  psk 另外的计算公式 
        (define (psk row col)
                (cond ((> col row) (error "input error!"))
                      ((or (= col row) (= col 0)) 1)
                        (else (+ (psk (- row 1) (- col 1))
                                (psk (- row 1) col)))))


        ;1.14  空间和步数增长的阶   ;; ----解决！   
        ; 类推法  类比法 逐步进行得得出规律 2n+1 O(n)
        ; 步数阶(O(n**x)和空间阶相同 x:硬币的种类)

        ;practive 1.15
        ;sinx = 3*sin(x/3)-4*(sin(x/3))**3  condition: angle<0.1 弧度

        (define (cube x) (* x x x))
        (define (p x    y) (- (* 3 x) (* 4 y)))
        (define (sine angles)
                (if (< (abs angles) 0.1)
                    angles
                    (p (sine (/ angles 3.0)) (cube (sine (/ angles 3.0))))
                    ))
        
        ;对于sine(p) p 执行了多少次？
        ;求幂 ;exponentiation
        (define (eve? n)
                (= (remainder n 2) 0))
        (define (expts b n)
                (cond ((= n 0) 1)
                        ((eve? n) (* (expts b (/ n 2)) (expts b (/ n 2))))
                        (else (* b (exptsb (- n 1))))
                ))
        ;; (expts 2 2) ->
        ;               (expts 2 1)**2 
        ;                        ->(2*(expts 2 0))**2 ->
        ;|空间O(n) 步阶 O(LGN+O(n**2)) //有待考虑
        


        ;;practice 1.16 (n**2)**（n/2）
        (define (expt_dd b n a)
                (cond ((= 0 n) a)
                        ((eve? n)  (expt_dd (* b b) (/ n 2) a))
                        (else (expt_dd b (- n 1) (* b a)))))
        ;; (3 2 1)->(9 1 1)*(9 1 1)->(9 0 9)*(9 0 9) = 9 * 9 = 81

; 8/2 16/2 4/2 14/2 28/2 56/2 112

        ;; practice 1.17

        (define (mul a b)
                ( cond ((= b 0) 0)
                        ((eve? b) (double (mul a (halve b))))
                        ((not(eve? b)) (+ a (mul a (- b 1)))
                        )))
        ;mul (3 2)-> (3 1)*2->(3+(3,0))*2-> ;1.17的正解


        ;;practice 1.18
        (define (double a) (* a 2))
        (define (halve a) (/ a 2))
        ; (define (expt_2? n)
        ;         (cond ((eve? n) ))
        (define (log_+ a b) (log_* a b 0))
        (define (log_* a b c)
                (cond ((= b 0) c)
                (else (if (eve? b) 
                        (log_*  (double a) (halve b) c)
                        (log_* a (- b 1) (+ c a))))))        
        ;log ( 3 6 3 0)-> (3 3 6 0)->(3 2 6 3) ->(3 1 12 3)
        ;log (3 5 3 0)->(3 4 3 3) ->(3 2 6 3) -> (3 1 12 3)                
        
        ;practice 1.19  (1 0 0 1)
        ;---# 0 1 1 2 3 5 8 13 ...   -> a=a+b b =a   b= 0 a= 1   (0 1)
        ;(1 0 0 1 1)->(1,1,0,1,0)->b = 1
        ;(1 0 0 1 2)->(1,0,p-,q-,1)(a*q+ap+b*q,b*p+a*q) ->(q+p,q)
        ;q+p = a    q =b  Tpq = (a*q+ap+b*q)  a = (a*q+ap+b*q) b =b*p +a*q
        ;-----> a*q+ap+b*q = a+b ->(a+b)*(q-1)+ap =a
        ;-----> b =b*p +a*q  b(1-p)=a*q 
        (define (fib n)
                (fib-iter 1 0 0 1 n))
        (define (fib-iter a b p q count)
                (cond ((= count 0) b)
                    ((eve? count) (fib-iter 
                        a
                        b
                        (+ (* p p) (* q q))
                        (+ (* 2 p q) (* q q))
                        (/ count 2)))
                    (else (fib-iter 
                        (+ (* b q) (* a p) (* a q))
                        (+ (* b p) (* a q))
                        p
                        q 
                        (- count 1)))
                ))
        
        ;practice 1.21
        (define (smallest-divisor n) (divisors n 2))
        (define (divisors n a)
                (cond ((= (remainder n a) 0) a)
                        ((> (* a a) n) n)
                    (else (divisors n (next a)))))
        (define (prime? n)
                (= (smallest-divisor n) n)
                ; (smallest-divisor n)
                )
        ;1.23
        (define (next n)
                (if (= n 2)
                        3
                        (+ n 2)))
        ;1.27
        (define (square x) (* x x))
        (define (expmod b n m)
                (cond ((= n 0) 1)
                (else (if (eve? n)
                        (remainder (square (expmod b (/ n 2) m)) m)
                        (remainder (* b (expmod b (- n 1) m)) m)))))
        (define (fm-test n)
                (= (expmod a n n) a))

        ;;1.28 ▲

        ;;1.29 辛普森 积分法(3/h*(y0+4y1+2y2+..2y2n-2 +4y2n-1+y2n)) 
        ;sum 递归法
        (define (sum term a nexts b)
                (if (> a b)
                        0
                        (+ (term a) (sum term (nexts a) nexts b))
                ))
        (define (xps f a b n)
                (define h (/ (- b a) n))
                (define (inc z) (+ z 1))
                (define (yk k) 
                        (if (or (= k 0) (= k n))
                                (f (+ a (* k h)))
                                (if (eve? k)
                                        (* 2 (f (+ a (* k h))))
                                        (* 4 (f (+ a (* k h))))
                                )))
                (* (sum_dd yk 0 inc n) (/ h 3.0))
        
        )
        ;;迭代法：
        (define (sum_dd term a nexts b)
                (define (iter a result)
                        (if (> a b)
                                result
                                (iter (nexts a) (+ result (term a)))
                ))
                (iter a 0))
        
        ;1.31
        ;迭代
        (define (product__dd term a nexts b)
                (define (iter a result)
                (if (> a b)
                        result
                        (iter (nexts a) (* result (term a)))
        ))
        (iter a 1))
        ;递归
        (define (inc z) (+ z 1))
        (define (self x) x)
        (define (product term a nexts b)
                (if (> a b)
                        1
                        (* (term a) (product term (nexts a) nexts b))
                        ))
        (define (pi b)
                (define (test x)
                        (+ x 2))
                ; (product self a inc b))
                (* (exact->inexact (/ (/ (product__dd square 2 test b) (* b 2)) (product__dd square 3 test b))) 4))
        ;;
        ;1.32
        ;【累积概念】抽取相同点
        (define (accumulate combiner null-value term a nexts b)
                        (if (> a b)
                                null-value
                                (combiner a (accumulate combiner null-value term (nexts a) nexts b))
                        ))
        ;迭代版
        (define (accumulate_dd combiner null-value term a nexts b)
                (define (iter a result)
                        (if (> a b)
                                result
                                (iter (nexts a) (combiner result (term a)))
                        ))
                        (iter a null-value))

        ;practice 1.33
        (define (fileter-ace combiner null-value term a nexts b valid?)
                        (if (> a b)
                                null-value
                                (let ((re (fileter-ace combiner null-value term (nexts a) nexts b valid?)))
                                (if (valid? a)
                                        (combiner (term a) re)
                                        re
                                )
                        )))
        (define (ss)
                (fileter-ace + 0 self 1 inc 10 prime?)
                )
        
        ;practice 1.35 
        
        
        ;practice 1.36 
        ;1.37      1.618032
        ;递归
        (define (cf k) (/ 1 (cont-frac_dd 1 (/ (N k) (D k) k) k)))
        (define (cont-frac n d k)
                (define (N n) 1.0)
                (define (D d) 1.0)
                (if (= k n)
                     (/ (N n) (D k))
                     (/ (N n) (+ (D d) (cont-frac (+ n 1) (+ d 1) k)))
                )
        )       
                ; (1 1 2)-> (n1/(d1+(2 2 2)))->(n1/(d1+(n2/d2)))
                ;(1 1 3) ->(n1/(d1+(2 2 3)))->(n1/(d1+(n2/(d2+(3 3 3)))))
        ;迭代
        (define (N n) 1.0)
        ; (define (D d) 1.0)
        
        (define (cont-frac_dd n r k)
                (if (= k 0)
                        r
                        (let ((dds 
                                 (cont-frac_dd (+ n 1) 
                                ;        (/ (N (- k 1)) (+ (/ (N (k) (D k))) (D (- k 1))))
                                        (/ (N (- k 1)) (+ (D (- k 1)) r))       
                                        (- k 1))))
                                        dds)
                                        )
                                ; (cont-frac_dd (+ n 1) )(/r (+ (D n) ))
                ; (+ (/ (N (k) (D k))) (D (- k 1)))
                )
        ; 1.38 ni =1 di =1 2 1 1 4 1 1 6 1 1 8 1 1 10 1...
                        ;     2     5    8     11
        ; (define (D i) 
        ;         (cond   ((= i 1) 1)
        ;                 ((= i 2) 2)
        ;                 ((= i 3) 1)
        ;             ((or (= 5 i) (= (remainder (- i 5) 3) 0)) (+ (D (- i 1)) (D (- i 2)) (D (- i 3))))
        ;             (else 1))) 
        (define (D i)
                (cond ((= (remainder (+ i 1) 3) 0) (/ (* 2 (+ i 1)) 3))
                        (else 1)))
        (define (eee k) (+ 2 (cont-frac_dd 1 (/ (N k) (D k) k) k)) )

        ;1.39 tanx  continue-fraction(分数)
        (define (tan-cf x d)
                (define (M i) (- (* 2 i) 1.0))
                (define (t-cf i)
                        (if (= i d) 
                                (/ (square x) (M i))
                                (cond   ((= i 1) (/ x (- (M i) (t-cf (+ i 1)))))
                                       (else (/ (square x) (- (M i) (t-cf (+ i 1))))))))
                ; (/ (t-cf 1) x)
                (t-cf 1)
        )
                                        

        (newline))