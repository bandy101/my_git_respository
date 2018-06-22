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
                (= (remainder 2 0) 0))
        (define (expts b n)
                (cond ((= n 0) 1)
                        ((eve? n) (* (expts b (/ n 2)) (expts b (/ n 2))))
                        (else (* b (exptsb (- n 1))))
                        
                ))

        (newline))        