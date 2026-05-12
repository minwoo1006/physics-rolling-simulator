import numpy as np
from vpython import sphere, box, vec, rate, color, canvas, cylinder, compound, button, slider, wtext, menu

# --- Physics Constants & Initial Defaults ---
G = 9.81
R_DEFAULT = 0.0254    # Billiard ball radius (m)
THETA_DEFAULT = 47.8  # degrees
MU_K_DEFAULT = 0.18
MU_S_DEFAULT = 0.20
D_RATIO_DEFAULT = 0.004

# --- Global State ---
running = False
reset_needed = False
t = 0
dt = 0.002
x = 0.0
v = 0.0
omega = 0.0

# Current Parameters
params = {
    "theta": np.radians(THETA_DEFAULT),
    "mu_k": MU_K_DEFAULT,
    "mu_s": MU_S_DEFAULT,
    "d_ratio": D_RATIO_DEFAULT,
    "R": R_DEFAULT
}

# --- Physics Calculations ---
def calculate_physics(v, omega, R, theta, mu_k, mu_s, D_R):
    """
    Calculates linear and angular acceleration based on current state.
    Returns: (a, alpha, is_sliding)
    """
    # State determination
    req_friction_ratio = (2/7) * np.tan(theta) + (5/7) * D_R
    
    is_sliding = False
    if abs(v - R * omega) < 1e-3:
        if req_friction_ratio > mu_s:
            is_sliding = True
    else:
        if v > R * omega:
            is_sliding = True
            
    if is_sliding:
        a = G * (np.sin(theta) - mu_k * np.cos(theta))
        alpha = (5/2) * (mu_k - D_R) * G * np.cos(theta) / R
    else:
        a = (5/7) * G * (np.sin(theta) - D_R * np.cos(theta))
        alpha = a / R
        
    return a, alpha, is_sliding

# --- UI and Main Loop Execution ---
if __name__ == "__main__":
    # --- UI Setup ---
    scene = canvas(title="<b>Rolling and Sliding Simulation Dashboard</b>", 
                   width=900, height=500, center=vec(0.3, -0.1, 0), background=color.gray(0.1),
                   userspin=True, userzoom=True) # Enable camera controls

    scene.append_to_caption("\n")

    # Real-time Metrics Display
    scene.append_to_caption("<b>Real-time Metrics:</b>\n")
    v_text = wtext(text="Linear Velocity (v): 0.00 m/s")
    scene.append_to_caption(" | ")
    w_text = wtext(text="R * Omega: 0.00 m/s")
    scene.append_to_caption(" | ")
    ratio_display = wtext(text="Ratio (v/Rw): 0.00")
    scene.append_to_caption("\n\n")

    # Control Functions
    def toggle_run(b):
        global running
        running = not running
        b.text = "Pause" if running else "Resume"

    def reset_sim(b):
        global t, x, v, omega, running, reset_needed
        t = 0
        x = 0
        v = 0
        omega = 0
        running = False
        run_btn.text = "Start"
        reset_needed = True

    def adjust_theta(s):
        params["theta"] = np.radians(s.value)
        theta_text.text = f" {s.value:1.1f}°"
        reset_sim(None)

    def adjust_mu(s):
        params["mu_k"] = s.value
        params["mu_s"] = s.value + 0.02 # Keep static slightly higher
        mu_text.text = f" {s.value:1.2f}"
        reset_sim(None)

    def adjust_d(s):
        params["d_ratio"] = s.value
        d_text.text = f" {s.value:1.3f}"
        reset_sim(None)

    # Buttons
    run_btn = button(text="Start", bind=toggle_run, pos=scene.caption_anchor)
    scene.append_to_caption("  ")
    button(text="Reset", bind=reset_sim, pos=scene.caption_anchor)
    scene.append_to_caption("\n\n")

    # Sliders
    scene.append_to_caption("Incline Angle: ")
    theta_slider = slider(min=0, max=70, value=THETA_DEFAULT, bind=adjust_theta)
    theta_text = wtext(text=f" {THETA_DEFAULT}°")
    scene.append_to_caption("\n")

    scene.append_to_caption("Friction (mu_k): ")
    mu_slider = slider(min=0.01, max=0.6, value=MU_K_DEFAULT, bind=adjust_mu)
    mu_text = wtext(text=f" {MU_K_DEFAULT}")
    scene.append_to_caption("\n")

    scene.append_to_caption("Normal Offset (D/R): ")
    d_slider = slider(min=0.0, max=0.1, value=D_RATIO_DEFAULT, bind=adjust_d)
    d_text = wtext(text=f" {D_RATIO_DEFAULT}")
    scene.append_to_caption("\n\n")

    # --- Graphs (Integrated in VPython) ---
    from vpython import graph, gcurve

    v_graph = graph(width=450, height=250, title="Velocity vs Time", xtitle="Time (s)", ytitle="v (m/s)", foreground=color.black, background=color.white)
    v_curve = gcurve(color=color.blue, label="Linear Velocity (v)")
    w_curve = gcurve(color=color.red, label="R * Omega")

    ratio_graph = graph(width=450, height=250, title="Ratio v / (R*omega)", xtitle="Time (s)", ytitle="Ratio", foreground=color.black, background=color.white, ymax=3, ymin=0)
    ratio_curve = gcurve(color=color.green)

    # --- Objects Construction ---
    def create_world():
        # Incline
        theta = params["theta"]
        dir_vec = vec(np.cos(theta), -np.sin(theta), 0)
        norm_vec = vec(np.sin(theta), np.cos(theta), 0)
        
        incline_len = 2.0
        incline_box = box(pos=dir_vec * (incline_len / 2) - norm_vec * 0.01,
                          size=vec(incline_len, 0.02, 0.3),
                          axis=dir_vec,
                          color=color.white, opacity=0.5)
        
        # Ball
        ball_sphere = sphere(pos=vec(0,0,0), radius=params["R"], color=color.red)
        marker = cylinder(pos=vec(0,0,params["R"]*0.8), axis=vec(0,0,params["R"]*0.4), radius=params["R"]*0.2, color=color.yellow)
        ball_comp = compound([ball_sphere, marker], pos=norm_vec * params["R"], make_trail=True, retain=100)
        
        return incline_box, ball_comp, dir_vec, norm_vec

    incline, ball, dir_vec, norm_vec = create_world()

    # --- Main Simulation Loop ---
    while True:
        rate(200)
        
        if reset_needed:
            # Cleanup
            incline.visible = False
            ball.visible = False
            ball.clear_trail()
            del incline, ball
            
            # Recreate
            incline, ball, dir_vec, norm_vec = create_world()
            
            # Clear graphs
            v_curve.delete()
            w_curve.delete()
            ratio_curve.delete()
            
            reset_needed = False
            
        if running:
            # Physics Step
            theta = params["theta"]
            mu_k = params["mu_k"]
            mu_s = params["mu_s"]
            D_R = params["d_ratio"]
            R = params["R"]
            
            a, alpha, is_sliding = calculate_physics(v, omega, R, theta, mu_k, mu_s, D_R)
                
            # Update
            v += a * dt
            omega += alpha * dt
            x += v * dt
            t += dt
            
            # VPython Update
            ball.pos = norm_vec * R + dir_vec * x
            ball.rotate(angle=omega * dt, axis=vec(0,0,-1))
            
            # Graph Update
            v_curve.plot(t, v)
            w_curve.plot(t, R * omega)
            
            # Numerical Display Update
            v_text.text = f"Linear Velocity (v): {v:1.2f} m/s"
            w_text.text = f"R * Omega: {R*omega:1.2f} m/s"
            
            if omega > 0:
                current_ratio = v / (R * omega)
                ratio_curve.plot(t, current_ratio)
                ratio_display.text = f"Ratio (v/Rw): {current_ratio:1.2f}"
                
            # Stop condition
            if x > 1.8:
                running = False
                run_btn.text = "Finished"

