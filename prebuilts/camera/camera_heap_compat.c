#include <malloc.h>

/* Preserve the verified provider-only heap policy used by the stock303 HAL. */
__attribute__((constructor)) static void disable_heap_pointer_tagging(void) {
    mallopt(M_BIONIC_SET_HEAP_TAGGING_LEVEL, M_HEAP_TAGGING_LEVEL_NONE);
}
