import streamlit as st
import time

if "tap_count" not in st.session_state:
    st.session_state.tap_count = 0
    st.session_state.last_tap_time = time.time()
    st.session_state.powerups = 3
    st.session_state.last_powerup_time = time.time()
    st.session_state.powerup_active = False
    st.session_state.powerup_end_time = 0
    st.session_state.tap_value = 1
    st.session_state.tap_level = 1
    st.session_state.energy = 1000
    st.session_state.max_energy = 1000
    st.session_state.last_energy_time = time.time()
    st.session_state.energy_upgrade_level = 1
    st.session_state.max_energy_level = 20
    st.session_state.energy_powerups = 3
    st.session_state.last_energy_powerup_time = time.time()

upgrade_costs = {
    1: 100, 2: 300, 3: 650, 4: 1000, 5: 1500,
    6: 2000, 7: 3500, 8: 5500, 9: 7000, 10: 12000,
    11: 15000, 12: 18000, 13: 20000, 14: 24000,
    15: 29000, 16: 34000, 17: 40000, 18: 45000,
    19: 51000, 20: 60000
}

energy_upgrade_costs = {
    1: 100, 2: 300, 3: 650, 4: 1000, 5: 1500,
    6: 2000, 7: 3500, 8: 5500, 9: 7000, 10: 12000,
    11: 15000, 12: 18000, 13: 20000, 14: 24000,
    15: 29000, 16: 34000, 17: 40000, 18: 45000,
    19: 51000, 20: 60000
}

current_time = time.time()
time_since_last_regen = current_time - st.session_state.last_energy_time
energy_regen = int(time_since_last_regen * 1)
st.session_state.energy = min(
    st.session_state.max_energy,
    st.session_state.energy + energy_regen
)
st.session_state.last_energy_time = current_time

if current_time - st.session_state.last_energy_powerup_time > 86400:
    st.session_state.energy_powerups = 3
    st.session_state.last_energy_powerup_time = current_time

if current_time - st.session_state.last_powerup_time > 86400:
    st.session_state.powerups = 3
    st.session_state.last_powerup_time = current_time

st.title("💰 Tap to Earn")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Points", value=st.session_state.tap_count)
with col2:
    st.metric(label="⚡ Energy", value=f"{st.session_state.energy}/{st.session_state.max_energy}")
with col3:
    st.metric(label="💪 Tap Power", value=f"Level {st.session_state.tap_level}")

st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
tap_button = st.button("✨ TAP HERE ✨", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

if tap_button:
    if st.session_state.energy >= st.session_state.tap_level:
        points_earned = st.session_state.tap_value
        if st.session_state.powerup_active:
            points_earned *= 10
        st.session_state.tap_count += points_earned
        st.session_state.energy -= st.session_state.tap_level
        st.session_state.last_tap_time = current_time
    else:
        st.warning("Not enough energy! Wait for it to regenerate.")

st.subheader("Upgrades")
upgrade_col1, upgrade_col2 = st.columns(2)

with upgrade_col1:
    st.write("**Tap Power Upgrade**")
    next_level = st.session_state.tap_level + 1
    if next_level in upgrade_costs:
        upgrade_cost = upgrade_costs[next_level]
        if st.button(
            f"⬆️ Level {next_level} (Cost: {upgrade_cost})",
            key="tap_upgrade",
            use_container_width=True
        ):
            if st.session_state.tap_count >= upgrade_cost:
                st.session_state.tap_count -= upgrade_cost
                st.session_state.tap_level = next_level
                st.session_state.tap_value = next_level
            else:
                st.warning("Not enough points to upgrade!")
    else:
        st.success("🚀 Max level reached!")

with upgrade_col2:
    st.write("**Energy Capacity Upgrade**")
    if st.session_state.energy_upgrade_level < st.session_state.max_energy_level:
        next_energy_level = st.session_state.energy_upgrade_level + 1
        energy_upgrade_cost = energy_upgrade_costs[next_energy_level]
        if st.button(
            f"⚡ Level {next_energy_level} (+500 Energy, Cost: {energy_upgrade_cost})",
            key="energy_upgrade",
            use_container_width=True
        ):
            if st.session_state.tap_count >= energy_upgrade_cost:
                st.session_state.tap_count -= energy_upgrade_cost
                st.session_state.max_energy += 500
                st.session_state.energy_upgrade_level += 1
            else:
                st.warning("Not enough points to upgrade!")
    else:
        st.success("🔋 Max Energy Level Reached!")

st.subheader("Power-ups")
powerup_col1, powerup_col2 = st.columns(2)

with powerup_col1:
    st.write("**Energy Refill**")
    st.write(f"Available: {st.session_state.energy_powerups}")
    if st.session_state.energy >= st.session_state.max_energy:
        st.button("Max Energy", disabled=True, key="energy_powerup_disabled", use_container_width=True)
    else:
        if st.button("⚡ Refill Energy", key="energy_powerup", use_container_width=True):
            if st.session_state.energy_powerups > 0:
                st.session_state.energy_powerups -= 1
                st.session_state.energy = st.session_state.max_energy
                st.success("Energy fully restored! 🔋")
            else:
                st.warning("No energy power-ups left!")

with powerup_col2:
    st.write("**Tap Booster**")
    st.write(f"Available: {st.session_state.powerups}")
    if st.session_state.powerup_active:
        time_left = max(0, st.session_state.powerup_end_time - current_time)
        st.button(
            f"Active ({int(time_left)}s)",
            disabled=True,
            key="powerup_active",
            use_container_width=True
        )
    else:
        if st.button("🔥 10x Boost (20s)", key="tap_powerup", use_container_width=True):
            if st.session_state.powerups > 0:
                st.session_state.powerups -= 1
                st.session_state.powerup_active = True
                st.session_state.powerup_end_time = current_time + 20
                st.success("Power-up activated! 10x points for 20 seconds! 🚀")
            else:
                st.warning("No power-ups left!")

if st.session_state.powerup_active and current_time > st.session_state.powerup_end_time:
    st.session_state.powerup_active = False
    st.experimental_rerun()
