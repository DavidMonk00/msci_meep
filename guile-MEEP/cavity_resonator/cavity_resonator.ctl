; Using a=100nm convention

(define-param r 1.25)
(define-param l 20)
(define-param s (* l r))
(define-param w 4)
(define-param d (/ l 16))
(define-param dpml (/ s 16))
(define-param sx s)
(define-param sy s)
(define-param fcen 0.2)
(define-param df 0.3)
(define-param res 16)
(define-param freq 0.14601667745703556)

(set-param! resolution res)
(set! eps-averaging? false)
(set! k-point (vector3 0 0 0))
(set! ensure-periodicity true)

(set! geometry-lattice (make lattice (size sx sy no-size)))
(define geom (list
  (make block
    (center 0 (/ (+ w d) 2))
    (size l d infinity)
    (material metal)
  )
  (make block
    (center 0 (/ (+ w d) -2))
    (size l d infinity)
    (material metal)
  )
  ; (make block
  ;   (center (/ (+ l d) 2))
  ;   (size d w infinity)
  ;   (material metal)
  ; )
  ; (make block
  ;   (center (/ (+ l d) -2))
  ;   (size d w infinity)
  ;   (material metal)
  ; )
))

(set! geometry geom)

(set! pml-layers (list (make pml
  (thickness dpml)
)))

(set! sources (list
  (make source
    (src (make continuous-src
      (frequency freq)
      (width 20)
      (end-time (/ 10 freq))
    ))
    (component Ez)
    (center 0)
    (size 2 4)
  )
))

(use-output-directory)

(run-until (/ 100 freq) (at-every 1 (output-png Ez "-Zc bluered")))
