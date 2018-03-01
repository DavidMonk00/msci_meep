(define-param w 10)
(define-param l 40)
(define-param h 10)
(define-param sx w)
(define-param sy l)
(define-param sz h)
(define-param stripH 0.5)
(define-param stripW 2)
(define-param dpml 0.5)
(define-param res 16)
(define-param freq 0.1)

(set-param! resolution res)
(set! eps-averaging? false)
(set! k-point (vector3 0 0 0))
; (set! ensure-periodicity true)

(set! geometry-lattice (make lattice (size sx sy sz)))
(define geom (list
  ; Substrate dielectric
  (make block
    (center 0 0 (/ h 4))
    (size infinity infinity (/ h 2))
    (material (make dielectric (epsilon 12)))
  )
  ; centre strip
  (make block
    (center 0 0 (/ stripH 2))
    (size stripW infinity stripH)
    (material metal)
  )
  ; ground plates
  (make block
    (center (/ (- w stripW) 2) 0 (/ stripH 2))
    (size stripW infinity stripH)
    (material metal)
  )
  (make block
    (center (/ (- w stripW) -2) 0 (/ stripH 2))
    (size stripW infinity stripH)
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
      (end-time (/ 10 freq))
    ))
    (component Ez)
    (center 0 (- (/ l 6) (/ l 2)) 3)
    (size (/ 0.5 freq) 0.5 0.5)
  )
))

(run-until (/ 50 freq)
  (to-appended "ez" (at-every 1 output-efield-z))
)
