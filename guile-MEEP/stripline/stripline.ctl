(define-param Xdim 10)
(define-param Ydim 60)
(define-param Zdim 10)
(define-param sx Xdim)
(define-param sy Ydim)
(define-param sz Zdim)
(define-param t 0.5)      ; Strip thickness
(define-param S 2)        ; Thickness of centre strip
(define-param W 2)        ; Width of gap
(define-param dpml 0.5)
(define-param res 8)
(define-param freq 0.1)

(set-param! resolution res)
(set! eps-averaging? false)
(set! k-point (vector3 0 0 0))
; (set! ensure-periodicity true)

(set! geometry-lattice (make lattice (size sx sy sz)))
(define geom (list
  ; Substrate dielectric
  (make block
    (center 0 0 (/ Zdim -4))
    (size infinity infinity (/ Zdim 2))
    (material (make dielectric (epsilon 12)))
  )
  ; centre strip
  (make block
    (center 0 0 (/ t 2))
    (size S infinity t)
    (material metal)
  )
  ; ground plates
  (make block
    (center (/ (- Xdim (+ (* 2 W) S)) 4) 0 (/ t 2))
    (size (/ (- Xdim (+ (* 2 W) S)) 2) infinity t)
    (material metal)
  )
  (make block
    (center (/ (- Xdim (+ (* 2 W) S)) -4) 0 (/ t 2))
    (size (/ (- Xdim (+ (* 2 W) S)) 2) infinity t)
    (material metal)
  )
))

(set! geometry geom)

(set! pml-layers (list (make pml
  (thickness dpml)
)))

(use-output-directory)

; source
(set! sources (list
  (make source
    (src (make continuous-src
      (frequency freq)
      (width 20)
      (end-time (/ 20 freq))
    ))
    (component Ez)
    (center 0 (- (/ Ydim 6) (/ Ydim 2)) 3)
    (size S 0 0)
  )
))

(run-until (/ 40 freq)
  (to-appended "ez" (at-every 1 output-efield-z))
)
