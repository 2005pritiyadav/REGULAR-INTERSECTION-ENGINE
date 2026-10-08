import streamlit as st

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Regular Intersection Engine",
    page_icon="🔄",
    layout="wide"
)

st.title("🔄 Regular Intersection Engine")
st.write(
    "Enter two DFAs and compute their cross-product DFA "
    "for the intersection language L(M1) ∩ L(M2)."
)

st.divider()


# ============================================================
# FUNCTION TO PARSE COMMA-SEPARATED INPUT
# ============================================================

def parse_list(text):
    return [x.strip() for x in text.split(",") if x.strip()]


# ============================================================
# FUNCTION TO CREATE TRANSITION TABLE
# ============================================================

def create_transition_table(states, alphabet, prefix):

    transitions = {}

    st.write("### Transition Function")

    for state in states:

        transitions[state] = {}

        cols = st.columns(len(alphabet) + 1)

        cols[0].write(f"**{state}**")

        for i, symbol in enumerate(alphabet):

            value = cols[i + 1].text_input(
                f"δ({state},{symbol})",
                key=f"{prefix}_{state}_{symbol}"
            )

            transitions[state][symbol] = value.strip()

    return transitions


# ============================================================
# VALIDATE DFA
# ============================================================

def validate_dfa(
    states,
    alphabet,
    start_state,
    final_states,
    transitions
):

    if len(states) == 0:
        return False, "States cannot be empty."

    if len(alphabet) == 0:
        return False, "Alphabet cannot be empty."

    if start_state not in states:
        return False, "Start state must belong to the set of states."

    for final_state in final_states:

        if final_state not in states:
            return False, f"Final state {final_state} is not in states."

    for state in states:

        if state not in transitions:
            return False, f"Missing transitions for state {state}."

        for symbol in alphabet:

            if symbol not in transitions[state]:
                return False, f"Missing transition for {state},{symbol}."

            destination = transitions[state][symbol]

            if destination == "":
                return False, (
                    f"Transition δ({state},{symbol}) is empty."
                )

            if destination not in states:
                return False, (
                    f"δ({state},{symbol}) = {destination}, "
                    f"but {destination} is not a valid state."
                )

    return True, "Valid DFA"


# ============================================================
# DFA 1 AND DFA 2 INPUT
# ============================================================

col1, col2 = st.columns(2)


# ============================================================
# DFA 1
# ============================================================

with col1:

    st.header("🟦 DFA 1")

    states1_text = st.text_input(
        "States of DFA 1",
        value="q0,q1,q2",
        key="states1"
    )

    alphabet1_text = st.text_input(
        "Alphabet of DFA 1",
        value="0,1",
        key="alphabet1"
    )

    start1 = st.text_input(
        "Start State of DFA 1",
        value="q0",
        key="start1"
    )

    final1_text = st.text_input(
        "Final States of DFA 1",
        value="q2",
        key="final1"
    )

    states1 = parse_list(states1_text)
    alphabet1 = parse_list(alphabet1_text)
    final1 = parse_list(final1_text)

    st.write("#### Enter Transitions")

    transitions1 = create_transition_table(
        states1,
        alphabet1,
        "dfa1"
    )


# ============================================================
# DFA 2
# ============================================================

with col2:

    st.header("🟩 DFA 2")

    states2_text = st.text_input(
        "States of DFA 2",
        value="p0,p1",
        key="states2"
    )

    alphabet2_text = st.text_input(
        "Alphabet of DFA 2",
        value="0,1",
        key="alphabet2"
    )

    start2 = st.text_input(
        "Start State of DFA 2",
        value="p0",
        key="start2"
    )

    final2_text = st.text_input(
        "Final States of DFA 2",
        value="p1",
        key="final2"
    )

    states2 = parse_list(states2_text)
    alphabet2 = parse_list(alphabet2_text)
    final2 = parse_list(final2_text)

    st.write("#### Enter Transitions")

    transitions2 = create_transition_table(
        states2,
        alphabet2,
        "dfa2"
    )


# ============================================================
# COMPUTE BUTTON
# ============================================================

st.divider()

compute = st.button(
    "🔄 Compute Intersection DFA",
    type="primary",
    use_container_width=True
)


# ============================================================
# COMPUTATION
# ============================================================

if compute:

    # --------------------------------------------------------
    # Check alphabets
    # --------------------------------------------------------

    if set(alphabet1) != set(alphabet2):

        st.error(
            "❌ The alphabets of DFA 1 and DFA 2 must be the same."
        )

        st.stop()


    # --------------------------------------------------------
    # Validate DFA 1
    # --------------------------------------------------------

    valid1, message1 = validate_dfa(
        states1,
        alphabet1,
        start1,
        final1,
        transitions1
    )


    # --------------------------------------------------------
    # Validate DFA 2
    # --------------------------------------------------------

    valid2, message2 = validate_dfa(
        states2,
        alphabet2,
        start2,
        final2,
        transitions2
    )


    if not valid1:

        st.error(f"❌ DFA 1 Error: {message1}")

        st.stop()


    if not valid2:

        st.error(f"❌ DFA 2 Error: {message2}")

        st.stop()


    st.success("✅ Both DFAs are valid!")


    # ========================================================
    # CROSS PRODUCT STATES
    # ========================================================

    st.divider()

    st.header("🎯 Intersection DFA")


    product_states = []

    for q in states1:

        for p in states2:

            product_states.append((q, p))


    # ========================================================
    # PRODUCT START STATE
    # ========================================================

    product_start = (start1, start2)


    # ========================================================
    # PRODUCT FINAL STATES
    # ========================================================

    product_final = []

    for q in states1:

        for p in states2:

            if q in final1 and p in final2:

                product_final.append((q, p))


    # ========================================================
    # PRODUCT TRANSITIONS
    # ========================================================

    product_transitions = {}

    for q, p in product_states:

        product_transitions[(q, p)] = {}

        for symbol in alphabet1:

            next_q = transitions1[q][symbol]

            next_p = transitions2[p][symbol]

            product_transitions[(q, p)][symbol] = (
                next_q,
                next_p
            )


    # ========================================================
    # DISPLAY PRODUCT STATES
    # ========================================================

    st.subheader("Product States")

    product_state_text = ", ".join(
        f"({q},{p})"
        for q, p in product_states
    )

    st.write(product_state_text)


    # ========================================================
    # DISPLAY START STATE
    # ========================================================

    st.write(
        f"**Start State:** "
        f"({product_start[0]},{product_start[1]})"
    )


    # ========================================================
    # DISPLAY FINAL STATES
    # ========================================================

    if product_final:

        final_text = ", ".join(
            f"({q},{p})"
            for q, p in product_final
        )

        st.write(
            f"**Final States:** {final_text}"
        )

    else:

        st.write(
            "**Final States:** None"
        )


    # ========================================================
    # TRANSITION TABLE
    # ========================================================

    st.subheader("Transition Table")

    table_data = []

    for state in product_states:

        row = {}

        q, p = state

        row["Product State"] = f"({q},{p})"

        for symbol in alphabet1:

            next_state = product_transitions[state][symbol]

            row[symbol] = (
                f"({next_state[0]},{next_state[1]})"
            )

        table_data.append(row)


    st.table(table_data)


    st.success(
        "✅ Cross-product DFA successfully created!"
    )


    # ========================================================
    # TEST A STRING
    # ========================================================

    st.divider()

    st.header("🧪 Test a String")

    test_string = st.text_input(
        "Enter a string to test",
        placeholder="Example: 0101",
        key="test_string"
    )

    test_button = st.button(
        "🔍 Test String"
    )


    if test_button:

        if test_string == "":

            st.warning(
                "⚠️ Please enter a string first."
            )

        else:

            current = product_start

            path = [current]

            valid_string = True


            # ------------------------------------------------
            # PROCESS STRING
            # ------------------------------------------------

            for symbol in test_string:

                if symbol not in alphabet1:

                    st.error(
                        f"❌ Invalid symbol '{symbol}'. "
                        f"Allowed symbols: "
                        f"{', '.join(alphabet1)}"
                    )

                    valid_string = False

                    break


                current = product_transitions[
                    current
                ][symbol]

                path.append(current)


            # ------------------------------------------------
            # DISPLAY RESULT
            # ------------------------------------------------

            if valid_string:

                st.subheader("State Traversal")

                path_text = " → ".join(
                    f"({q},{p})"
                    for q, p in path
                )

                st.info(path_text)


                if current in product_final:

                    st.success(
                        f"✅ ACCEPTED\n\n"
                        f"Final state reached: "
                        f"({current[0]},{current[1]})"
                    )

                else:

                    st.error(
                        f"❌ REJECTED\n\n"
                        f"Current state: "
                        f"({current[0]},{current[1]})"
                    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Regular Intersection Engine | "
    "Cross-Product Construction of DFA"
)