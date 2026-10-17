import streamlit as st
from itertools import product

st.set_page_config(
    page_title="Regular Intersection Engine",
    page_icon="🔄",
    layout="wide"
)

st.title("🔄 Regular Intersection Engine")
st.write(
    "Input two DFAs (M1 and M2) and compute their cross-product DFA "
    "for the intersection language L(M1) ∩ L(M2)."
)

st.divider()


# ---------------------------------------------------------
# FUNCTION TO READ DFA
# ---------------------------------------------------------

def parse_dfa(states_text, alphabet_text, start_state, final_text, transitions_text):

    states = {x.strip() for x in states_text.split(",") if x.strip()}
    alphabet = {x.strip() for x in alphabet_text.split(",") if x.strip()}
    final_states = {x.strip() for x in final_text.split(",") if x.strip()}
    start_state = start_state.strip()

    errors = []

    # Check states
    if not states:
        errors.append("States cannot be empty.")

    # Check alphabet
    if not alphabet:
        errors.append("Alphabet cannot be empty.")

    # Check start state
    if start_state not in states:
        errors.append(f"Start state '{start_state}' is not present in states.")

    # Check final states
    for state in final_states:
        if state not in states:
            errors.append(
                f"Final state '{state}' is not present in states."
            )

    transitions = {}

    lines = transitions_text.strip().splitlines()

    for line_number, line in enumerate(lines, start=1):

        if not line.strip():
            continue

        parts = [x.strip() for x in line.split(",")]

        if len(parts) != 3:
            errors.append(
                f"Transition line {line_number} must be: state,symbol,next_state"
            )
            continue

        current, symbol, next_state = parts

        if current not in states:
            errors.append(
                f"Line {line_number}: state '{current}' does not exist."
            )

        if symbol not in alphabet:
            errors.append(
                f"Line {line_number}: symbol '{symbol}' is not in alphabet."
            )

        if next_state not in states:
            errors.append(
                f"Line {line_number}: next state '{next_state}' does not exist."
            )

        transitions[(current, symbol)] = next_state

    # Check DFA completeness
    for state in states:
        for symbol in alphabet:
            if (state, symbol) not in transitions:
                errors.append(
                    f"Missing transition: δ({state}, {symbol})"
                )

    return {
        "states": states,
        "alphabet": alphabet,
        "start": start_state,
        "final": final_states,
        "transitions": transitions
    }, errors


# ---------------------------------------------------------
# PREDEFINED BINARY DFAs
# ---------------------------------------------------------

PRESETS = {
    "Ends with 10": {
        "states": "q0,q1,q2",
        "alphabet": "0,1",
        "start": "q0",
        "final": "q2",
        "transitions": "q0,0,q0\nq0,1,q1\nq1,0,q2\nq1,1,q1\nq2,0,q0\nq2,1,q1",
    },
    "Even number of 0s": {
        "states": "p0,p1",
        "alphabet": "0,1",
        "start": "p0",
        "final": "p0",
        "transitions": "p0,0,p1\np0,1,p0\np1,0,p0\np1,1,p1",
    },
    "Starts with 1": {
        "states": "s0,s1,dead",
        "alphabet": "0,1",
        "start": "s0",
        "final": "s1",
        "transitions": "s0,0,dead\ns0,1,s1\ns1,0,s1\ns1,1,s1\ndead,0,dead\ndead,1,dead",
    },
    "Contains 11": {
        "states": "a0,a1,a2",
        "alphabet": "0,1",
        "start": "a0",
        "final": "a2",
        "transitions": "a0,0,a0\na0,1,a1\na1,0,a0\na1,1,a2\na2,0,a2\na2,1,a2",
    },
    "Ends with 01": {
        "states": "r0,r1,r2",
        "alphabet": "0,1",
        "start": "r0",
        "final": "r2",
        "transitions": "r0,0,r1\nr0,1,r0\nr1,0,r1\nr1,1,r2\nr2,0,r1\nr2,1,r0",
    },
}


def fill_dfa(prefix, name):
    p = PRESETS[name]
    st.session_state[f"{prefix}_states"] = p["states"]
    st.session_state[f"{prefix}_alphabet"] = p["alphabet"]
    st.session_state[f"{prefix}_start"] = p["start"]
    st.session_state[f"{prefix}_final"] = p["final"]
    st.session_state[f"{prefix}_transitions"] = p["transitions"]


def load_preset(prefix):
    fill_dfa(prefix, st.session_state[f"{prefix}_choice"])


def load_demo():
    fill_dfa("m1", "Ends with 10")
    fill_dfa("m2", "Even number of 0s")
    st.session_state["m1_choice"] = "Ends with 10"
    st.session_state["m2_choice"] = "Even number of 0s"


# ---------------------------------------------------------
# DFA INPUT
# ---------------------------------------------------------

st.button(
    "⚡ Load demo: 'Ends with 10' ∩ 'Even number of 0s'",
    on_click=load_demo
)

col1, col2 = st.columns(2)


with col1:

    st.header("DFA M1")

    st.selectbox("Predefined DFA", list(PRESETS), key="m1_choice")
    st.button("📥 Load into M1", on_click=load_preset, args=("m1",))

    m1_states = st.text_input(
        "States of M1",
        placeholder="q0,q1,q2",
        key="m1_states"
    )

    m1_alphabet = st.text_input(
        "Alphabet of M1",
        placeholder="0,1",
        key="m1_alphabet"
    )

    m1_start = st.text_input(
        "Start State of M1",
        placeholder="q0",
        key="m1_start"
    )

    m1_final = st.text_input(
        "Final States of M1",
        placeholder="q2",
        key="m1_final"
    )

    m1_transitions = st.text_area(
        "Transitions of M1",
        placeholder="q0,0,q1\nq0,1,q0\nq1,0,q2\nq1,1,q0\nq2,0,q2\nq2,1,q2",
        height=180,
        key="m1_transitions"
    )


with col2:

    st.header("DFA M2")

    st.selectbox("Predefined DFA", list(PRESETS), index=1, key="m2_choice")
    st.button("📥 Load into M2", on_click=load_preset, args=("m2",))

    m2_states = st.text_input(
        "States of M2",
        placeholder="p0,p1",
        key="m2_states"
    )

    m2_alphabet = st.text_input(
        "Alphabet of M2",
        placeholder="0,1",
        key="m2_alphabet"
    )

    m2_start = st.text_input(
        "Start State of M2",
        placeholder="p0",
        key="m2_start"
    )

    m2_final = st.text_input(
        "Final States of M2",
        placeholder="p1",
        key="m2_final"
    )

    m2_transitions = st.text_area(
        "Transitions of M2",
        placeholder="p0,0,p0\np0,1,p1\np1,0,p0\np1,1,p1",
        height=180,
        key="m2_transitions"
    )


st.divider()

calculate = st.button(
    "⚙️ Compute Intersection DFA",
    type="primary",
    use_container_width=True
)


# ---------------------------------------------------------
# COMPUTE CROSS PRODUCT
# ---------------------------------------------------------

# Remember that the user pressed Compute, so results stay visible
# when the "Test String" button below triggers a rerun.
if calculate:
    st.session_state["computed"] = True

if st.session_state.get("computed"):

    m1, errors1 = parse_dfa(
        m1_states,
        m1_alphabet,
        m1_start,
        m1_final,
        m1_transitions
    )

    m2, errors2 = parse_dfa(
        m2_states,
        m2_alphabet,
        m2_start,
        m2_final,
        m2_transitions
    )

    all_errors = errors1 + errors2

    # Alphabet must be same
    if m1["alphabet"] != m2["alphabet"]:
        all_errors.append(
            "M1 and M2 must have the same alphabet for intersection."
        )

    if all_errors:

        st.error("❌ Invalid DFA Input")

        for error in all_errors:
            st.write("•", error)

    else:

        st.success("✅ Both DFAs are valid.")

        # Product states
        product_states = list(
            product(
                sorted(m1["states"]),
                sorted(m2["states"])
            )
        )

        # Start state
        product_start = (
            m1["start"],
            m2["start"]
        )

        # Final states = F1 × F2
        product_final = [
            (q, p)
            for q in sorted(m1["final"])
            for p in sorted(m2["final"])
        ]

        # Product transitions
        product_transitions = {}

        for q, p in product_states:

            for symbol in sorted(m1["alphabet"]):

                next_q = m1["transitions"][(q, symbol)]
                next_p = m2["transitions"][(p, symbol)]

                product_transitions[
                    ((q, p), symbol)
                ] = (next_q, next_p)

        st.divider()

        st.header("🎯 Cross-Product DFA")

        st.subheader("Product States")

        state_text = ", ".join(
            f"({q},{p})"
            for q, p in product_states
        )

        st.code(state_text)

        st.write(
            "**Start State:**",
            f"({product_start[0]},{product_start[1]})"
        )

        final_text_out = ", ".join(
            f"({q},{p})"
            for q, p in product_final
        )

        st.write(
            "**Final States:**",
            final_text_out if final_text_out else "None"
        )

        # Transition table
        st.subheader("Transition Table")

        table_data = []

        for state in product_states:

            row = {
                "Product State": f"({state[0]},{state[1]})"
            }

            for symbol in sorted(m1["alphabet"]):

                next_state = product_transitions[
                    (state, symbol)
                ]

                row[symbol] = (
                    f"({next_state[0]},{next_state[1]})"
                )

            table_data.append(row)

        st.dataframe(
            table_data,
            use_container_width=True,
            hide_index=True
        )

        st.success(
            "The cross-product DFA represents "
            "L(M1) ∩ L(M2)."
        )

        # -------------------------------------------------
        # STRING TEST
        # -------------------------------------------------

        st.divider()

        st.header("🧪 Test a String")

        test_string = st.text_input(
            "Enter a string",
            placeholder="Example: 0101"
        )

        if st.button("🔍 Test String"):

            current = product_start
            valid = True

            for symbol in test_string:

                if symbol not in m1["alphabet"]:

                    st.error(
                        f"❌ Invalid symbol '{symbol}' "
                        "in input string."
                    )

                    valid = False
                    break

                current = product_transitions[
                    (current, symbol)
                ]

            if valid:

                if current in product_final:

                    st.success(
                        f"✅ ACCEPTED — Final state reached: "
                        f"({current[0]},{current[1]})"
                    )

                else:

                    st.error(
                        f"❌ REJECTED — Final state not reached. "
                        f"Current state: ({current[0]},{current[1]})"
                    )
