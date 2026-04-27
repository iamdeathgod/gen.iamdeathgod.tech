import re

with open("index.html", "r") as f:
    content = f.read()

# Fix the XSS vulnerability by escaping HTML entities and also fix the animation-delay classes
content = content.replace('span class="text-[10px] text-white line-clamp-3">${prompt}</span>', 'span class="text-[10px] text-white line-clamp-3"></span>')

# Add the textContent assignment logic
replacement = """
      item.innerHTML = `
        <img src="${src}" alt="Generated artwork" class="w-full h-full object-cover" />
        <div class="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center p-2 text-center">
          <span class="text-[10px] text-white line-clamp-3"></span>
        </div>
      `;
      // Prevent XSS
      item.querySelector('span').textContent = prompt;
"""

content = re.sub(r'item\.innerHTML = `[\s\S]*?`;', replacement, content)

# Fix Tailwind config for animation delay
tailwind_config_fix = """
          keyframes: {
            blob: {
              '0%': { transform: 'translate(0px, 0px) scale(1)' },
              '33%': { transform: 'translate(30px, -50px) scale(1.1)' },
              '66%': { transform: 'translate(-20px, 20px) scale(0.9)' },
              '100%': { transform: 'translate(0px, 0px) scale(1)' },
            }
          }
        }
      }
    }
  </script>
  <style type="text/tailwindcss">
    @layer utilities {
      .animation-delay-2000 {
        animation-delay: 2s;
      }
      .animation-delay-4000 {
        animation-delay: 4s;
      }
    }
  </style>"""

content = content.replace("""
          keyframes: {
            blob: {
              '0%': { transform: 'translate(0px, 0px) scale(1)' },
              '33%': { transform: 'translate(30px, -50px) scale(1.1)' },
              '66%': { transform: 'translate(-20px, 20px) scale(0.9)' },
              '100%': { transform: 'translate(0px, 0px) scale(1)' },
            }
          }
        }
      }
    }
  </script>""", tailwind_config_fix)


with open("index.html", "w") as f:
    f.write(content)
