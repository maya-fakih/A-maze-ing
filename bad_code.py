# Go back to project root
cd ../../

# Create a Python file with BAD style
cat > bad_style.py << 'EOF'
# This has bad style!
def very_long_function_name_with_many_characters_that_exceeds_eighty_eight_characters_in_length(x):
    y= x+5  # Bad spacing
    z = y*2# No space after comment
    return z
EOF
