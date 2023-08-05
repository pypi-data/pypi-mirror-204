// Copyright 2021 The TensorStore Authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#ifndef TENSORSTORE_UTIL_GARBAGE_COLLECTION_PROTOBUF_H_
#define TENSORSTORE_UTIL_GARBAGE_COLLECTION_PROTOBUF_H_

#include <type_traits>

#include "google/protobuf/message_lite.h"
#include "tensorstore/util/garbage_collection/fwd.h"

namespace tensorstore {
namespace garbage_collection {

template <typename T>
struct GarbageCollection<
    T, std::enable_if_t<std::is_base_of_v<google::protobuf::MessageLite, T>>> {
  constexpr static bool required() { return false; }
};

}  // namespace garbage_collection
}  // namespace tensorstore

#endif  // TENSORSTORE_UTIL_GARBAGE_COLLECTION_PROTOBUF_H_
