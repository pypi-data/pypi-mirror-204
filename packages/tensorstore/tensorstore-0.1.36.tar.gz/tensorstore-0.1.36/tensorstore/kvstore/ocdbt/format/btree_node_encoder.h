// Copyright 2022 The TensorStore Authors
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

#ifndef TENSORSTORE_KVSTORE_OCDBT_FORMAT_BTREE_NODE_ENCODER_H_
#define TENSORSTORE_KVSTORE_OCDBT_FORMAT_BTREE_NODE_ENCODER_H_

#include <string>
#include <string_view>
#include <vector>

#include "absl/strings/cord.h"
#include "tensorstore/kvstore/ocdbt/format/btree.h"
#include "tensorstore/kvstore/ocdbt/format/config.h"
#include "tensorstore/util/result.h"

namespace tensorstore {
namespace internal_ocdbt {

struct EncodedNodeInfo {
  /// Full key of encoded node.
  std::string inclusive_min_key;

  /// Length of prefix of `inclusive_min_key` that is excluded from the encoded
  /// representation.
  KeyLength excluded_prefix_length;

  /// Statistics for the encoded node.
  BtreeNodeStatistics statistics;
};

/// Encoded b+tree node, generated by `BtreeNodeEncoder`.
struct EncodedNode {
  /// Encoded representation.
  absl::Cord encoded_node;

  EncodedNodeInfo info;
};

/// Encodes a sequence of b+tree nodes at a given height.
///
/// \tparam Entry Either `LeafNodeEntry` or `InteriorNodeEntry`.
template <typename Entry>
class BtreeNodeEncoder {
  static_assert(std::is_same_v<Entry, LeafNodeEntry> ||
                std::is_same_v<Entry, InteriorNodeEntry>);

 public:
  /// Constructs a b+tree node encoder.
  ///
  /// \param config Database configuration to use.
  /// \param height Height of the nodes being encoded.  Must be 0 if, and only
  ///     if, `Entry` is equal to `LeafNodeEntry`.
  /// \param existing_prefix Implicit key prefix for all existing entries.
  BtreeNodeEncoder(const Config& config, BtreeNodeHeight height,
                   std::string_view existing_prefix);

  /// Adds a new or existing entry.
  ///
  /// If `existing == true`, the `existing_prefix` passed to the constructor is
  /// prepended to `entry.key`.
  ///
  /// The `entry.key` `string_view` value is not copied, and must remain valid
  /// until after `Finalize` is called.
  void AddEntry(bool existing, Entry&& entry);

  /// Generates the encoded representation.
  ///
  /// \param may_be_root Indicates whether this may be the root node.  If `true`
  ///     and only a single `EncodedNode` is returned, it is guaranteed that the
  ///     `EncodedNode::excluded_prefix_length` of the returned node is equal to
  ///     `0`.  This is needed because no prefix is supported for the root node.
  Result<std::vector<EncodedNode>> Finalize(bool may_be_root);

  // Treat as private:

  struct BufferedEntry {
    // Length of the common prefix of this entry and the previous entry.
    size_t common_prefix_with_next_entry_length;
    bool existing;
    Entry entry;
    size_t cumulative_size;
  };

 private:
  const Config& config_;
  BtreeNodeHeight height_;
  std::string_view existing_prefix_;

  std::vector<BufferedEntry> buffered_entries_;
  size_t common_prefix_length_ = 0;
};

using BtreeLeafNodeEncoder = BtreeNodeEncoder<LeafNodeEntry>;
using BtreeInteriorNodeEncoder = BtreeNodeEncoder<InteriorNodeEntry>;

/// Adds a new interior node entry.
///
/// This is a convenience interface that simply forwards to
/// `BtreeNodeEncoder::AddEntry`.
void AddNewInteriorEntry(BtreeNodeEncoder<InteriorNodeEntry>& encoder,
                         const InteriorNodeEntryData<std::string>& entry);

}  // namespace internal_ocdbt
}  // namespace tensorstore

#endif  // TENSORSTORE_KVSTORE_OCDBT_FORMAT_BTREE_NODE_ENCODER_H_
